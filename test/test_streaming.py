# coding: utf-8

"""Tests for vpcloud_client.streaming. No network: every call goes through
httpx.MockTransport."""

import asyncio
import base64
import datetime
import json
import struct

import httpx
import pytest

import vpcloud_client
from vpcloud_client.credentials import AuthenticationError
from vpcloud_client.streaming import (
    TAIL_PROCEDURE,
    WATCH_PROCEDURE,
    ConnectError,
    atail,
    awatch,
    tail,
    watch,
)

BASE_URL = "http://observatory.test"
STREAM_HEADERS = {"content-type": "application/connect+json"}
UTC = datetime.timezone.utc


def envelope(message, flags=0):
    payload = message if isinstance(message, bytes) else json.dumps(message).encode()
    return struct.pack(">BI", flags, len(payload)) + payload


def end_stream(error=None, metadata=None):
    body = {}
    if error is not None:
        body["error"] = error
    if metadata is not None:
        body["metadata"] = metadata
    return envelope(body, flags=0x02)


def b64json(value):
    return base64.b64encode(json.dumps(value).encode()).decode()


def odd_chunks(data, sizes=(1, 3, 7, 2, 11)):
    """Split data into chunks that cut through envelope headers and payloads."""
    sizes = list(sizes)
    out, i, n = [], 0, 0
    while i < len(data):
        size = sizes[n % len(sizes)]
        out.append(data[i:i + size])
        i += size
        n += 1
    return out


class ChunkStream(httpx.SyncByteStream, httpx.AsyncByteStream):
    """A response body yielding the given chunks (or an endless generator),
    recording whether httpx closed it."""

    def __init__(self, chunks):
        self._chunks = chunks
        self.closed = False

    def _iter(self):
        return self._chunks() if callable(self._chunks) else iter(self._chunks)

    def __iter__(self):
        yield from self._iter()

    async def __aiter__(self):
        for chunk in self._iter():
            yield chunk

    def close(self):
        self.closed = True

    async def aclose(self):
        self.closed = True


def stream_response(data, status=200, headers=None):
    stream = data if isinstance(data, ChunkStream) else ChunkStream(odd_chunks(data))
    return httpx.Response(status, headers=headers if headers is not None else STREAM_HEADERS, stream=stream)


class Recorder:
    """MockTransport handler serving one queued response per request."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def __call__(self, request):
        self.requests.append(request)
        return self.responses.pop(0)

    def bodies(self):
        out = []
        for request in self.requests:
            flags, length = struct.unpack(">BI", request.content[:5])
            assert flags == 0
            assert length == len(request.content) - 5
            out.append(json.loads(request.content[5:]))
        return out


def config(**kwargs):
    kwargs.setdefault("observatory_access_token", "obs-token")
    return vpcloud_client.Configuration(**kwargs)


def sync_http(handler, base_url=BASE_URL):
    return httpx.Client(base_url=base_url, transport=httpx.MockTransport(handler))


def async_http(handler):
    return httpx.AsyncClient(base_url=BASE_URL, transport=httpx.MockTransport(handler))


def open_watch(handler, queries="DCGM_FI_DEV_GPU_UTIL", **kwargs):
    kwargs.setdefault("cluster_id", "c-1")
    return watch(config(), queries, http=sync_http(handler), **kwargs)


MATRIX = [{"metric": {"gpu": "0"}, "values": [[1700000000, "42"]]}]
SAMPLES = {
    "samples": {"name": "q0", "result": {"resultType": "matrix", "resultJson": b64json(MATRIX)}},
    "cursor": "v1:1",
}
CHANGE = {
    "change": {
        "name": "idle",
        "time": "2026-10-21T09:00:00.123456789Z",
        "appearedJson": [b64json({"metric": {"gpu": "1"}, "value": [1700000000, "3"]})],
        "disappearedJson": [b64json({"gpu": "2"})],
    },
    "cursor": "v1:2",
}
WATCH_HEARTBEAT = {"heartbeat": {}, "cursor": "v1:2"}


def test_request_is_one_enveloped_json_message_with_connect_headers():
    handler = Recorder(stream_response(end_stream()))
    with open_watch(handler, step="15s") as stream:
        assert list(stream) == []

    (request,) = handler.requests
    assert request.method == "POST"
    assert request.url.path == WATCH_PROCEDURE == "/observatory.v1.MetricsService/Watch"
    assert request.headers["content-type"] == "application/connect+json"
    assert request.headers["connect-protocol-version"] == "1"
    assert request.headers["authorization"] == "Bearer obs-token"
    assert "connect-accept-encoding" not in request.headers
    assert handler.bodies() == [{
        "queries": [{"name": "q0", "query": "DCGM_FI_DEV_GPU_UTIL"}],
        "mode": "WATCH_MODE_SAMPLES", "clusterId": "c-1", "step": "15s",
    }]


@pytest.mark.parametrize("queries, expected", [
    ("up", [{"name": "q0", "query": "up"}]),
    (["up", "down"], [{"name": "q0", "query": "up"}, {"name": "q1", "query": "down"}]),
    ({"iops": "sum(iops)", "bw": "sum(bw)"}, [{"name": "iops", "query": "sum(iops)"}, {"name": "bw", "query": "sum(bw)"}]),
])
def test_query_forms(queries, expected):
    handler = Recorder(stream_response(end_stream()))
    list(watch(config(), queries, http=sync_http(handler)))
    assert handler.bodies()[0]["queries"] == expected


def test_org_wide_watch_has_no_cluster_and_changes_mode():
    handler = Recorder(stream_response(end_stream()))
    list(watch(config(), "up", mode="changes", step=30, http=sync_http(handler)))
    body = handler.bodies()[0]
    assert "clusterId" not in body
    assert body["mode"] == "WATCH_MODE_CHANGES"
    assert body["step"] == "30s"


def test_bad_arguments():
    with pytest.raises(ValueError, match="mode"):
        watch(config(), "up", mode="everything", http=sync_http(Recorder()))
    with pytest.raises(ValueError, match="at least one query"):
        watch(config(), [], http=sync_http(Recorder()))
    with pytest.raises(ValueError, match="cluster_id"):
        tail(config(), "*", cluster_id="", http=sync_http(Recorder()))
    with pytest.raises(ValueError, match="timezone-aware"):
        tail(config(), "*", cluster_id="c-1", since=datetime.datetime(2026, 1, 1), http=sync_http(Recorder()))
    with pytest.raises(TypeError, match="ApiClient or Configuration"):
        watch(httpx.Client(base_url=BASE_URL), "up")


def test_api_client_and_configuration_both_work():
    for client in (config(), vpcloud_client.ApiClient(config())):
        handler = Recorder(stream_response(end_stream()))
        list(watch(client, "up", http=sync_http(handler)))
        assert handler.requests[0].headers["authorization"] == "Bearer obs-token"


def test_default_http_targets_observatory_host():
    stream = watch(config(observatory_host="https://beta.observatory.voltagepark.com"), "up")
    assert str(stream._http.base_url) == "https://beta.observatory.voltagepark.com"
    stream.close()
    assert stream._http.is_closed


def test_harbor_token_is_never_sent(monkeypatch):
    for k in ("VPCLOUD_CLIENT_ID", "VPCLOUD_CLIENT_SECRET", "VPCLOUD_OBSERVATORY_ACCESS_TOKEN"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("HOME", "/nonexistent")
    handler = Recorder(stream_response(end_stream()))
    stream = watch(vpcloud_client.Configuration(access_token="harbor-token"), "up", http=sync_http(handler))
    with pytest.raises(AuthenticationError):
        list(stream)
    assert handler.requests == []


def test_token_is_fetched_per_connect():
    tokens = iter(["Bearer t1", "Bearer t2"])
    cfg = config()
    cfg.auth_settings = lambda service=None: {"bearerAuth": {"value": next(tokens)}}
    handler = Recorder(
        stream_response(envelope(SAMPLES) + end_stream(error={"code": "unavailable", "message": "draining"})),
        stream_response(end_stream()),
    )
    list(watch(cfg, "up", http=sync_http(handler), reconnect=True, reconnect_backoff=0, max_reconnect_attempts=0))
    assert [r.headers["authorization"] for r in handler.requests] == ["Bearer t1", "Bearer t2"]


def test_streaming_timeout_is_a_read_timeout_not_a_total():
    handler = Recorder(stream_response(end_stream()))
    list(open_watch(handler, read_timeout=45))
    timeout = handler.requests[0].extensions["timeout"]
    assert timeout["read"] == 45
    assert timeout["connect"] == 10


def test_base_url_path_prefix_is_kept():
    handler = Recorder(stream_response(end_stream()))
    list(tail(config(), "*", cluster_id="c-1", http=sync_http(handler, base_url="http://gw.test/observatory")))
    assert handler.requests[0].url.path == "/observatory" + TAIL_PROCEDURE


def test_parses_messages_split_across_chunk_boundaries_and_skips_heartbeats():
    data = envelope(SAMPLES) + envelope(WATCH_HEARTBEAT) + envelope(CHANGE) + end_stream()
    for sizes in [(1,), (2, 5), (3, 7, 1, 13), (len(data),)]:
        handler = Recorder(stream_response(ChunkStream(odd_chunks(data, sizes))))
        with open_watch(handler) as stream:
            events = list(stream)
            assert stream.cursor == "v1:2"

        assert [e.kind for e in events] == ["samples", "change"]
        samples, change = events
        assert samples.name == "q0"
        assert samples.result_type == "matrix"
        assert samples.result == MATRIX
        assert samples.cursor == "v1:1"
        assert change.name == "idle"
        assert change.time == datetime.datetime(2026, 10, 21, 9, 0, 0, 123456, tzinfo=UTC)
        assert change.appeared == [{"metric": {"gpu": "1"}, "value": [1700000000, "3"]}]
        assert change.disappeared == [{"gpu": "2"}]


def test_samples_series():
    (event,) = list(open_watch(Recorder(stream_response(envelope(SAMPLES) + end_stream()))))
    (series,) = event.series()
    assert series.labels == {"gpu": "0"}
    assert [(s.timestamp, s.value) for s in series.samples] == [(1700000000.0, 42.0)]


def test_include_heartbeats_yields_them():
    data = envelope(WATCH_HEARTBEAT) + envelope(SAMPLES) + end_stream()
    events = list(open_watch(Recorder(stream_response(data)), include_heartbeats=True))
    assert [e.kind for e in events] == ["heartbeat", "samples"]
    assert events[0].is_heartbeat
    assert events[0].series() == []


def test_end_stream_ok_exposes_trailers():
    data = envelope(SAMPLES) + end_stream(metadata={"x-trace": ["abc"]})
    with open_watch(Recorder(stream_response(data))) as stream:
        assert len(list(stream)) == 1
        assert stream.trailers == {"x-trace": ["abc"]}
        assert stream.response_headers["content-type"] == "application/connect+json"


def test_end_stream_error_raises_connect_error_after_earlier_messages():
    details = [{"type": "google.rpc.ErrorInfo", "value": "AAAA"}]
    data = envelope(SAMPLES) + end_stream(
        error={"code": "permission_denied", "message": "cluster not in org", "details": details},
        metadata={"x-trace": ["abc"]},
    )
    received = []
    with pytest.raises(ConnectError) as info:
        for event in open_watch(Recorder(stream_response(data))):
            received.append(event)
    assert [e.kind for e in received] == ["samples"]
    err = info.value
    assert (err.code, err.message, err.details, err.metadata, err.http_status) == (
        "permission_denied", "cluster not in org", details, {"x-trace": ["abc"]}, None)
    assert str(err) == "permission_denied: cluster not in org"


def test_non_200_connect_json_error():
    response = httpx.Response(401, json={"code": "unauthenticated", "message": "invalid API token"})
    with pytest.raises(ConnectError) as info:
        list(open_watch(Recorder(response)))
    assert (info.value.code, info.value.message, info.value.http_status) == ("unauthenticated", "invalid API token", 401)


def test_non_200_without_connect_body_maps_http_status():
    response = httpx.Response(503, text="upstream connect error")
    with pytest.raises(ConnectError) as info:
        list(tail(config(), "*", cluster_id="c-1", http=sync_http(Recorder(response))))
    assert (info.value.code, info.value.message, info.value.http_status) == ("unavailable", "upstream connect error", 503)


def test_unexpected_content_type_is_an_error():
    response = httpx.Response(200, headers={"content-type": "text/html"}, text="<html>")
    with pytest.raises(ConnectError, match="unexpected content-type"):
        list(open_watch(Recorder(response)))


def test_compressed_message_is_rejected():
    data = envelope(b"\x1f\x8b-not-really-gzip", flags=0x01) + end_stream()
    with pytest.raises(ConnectError, match="compressed") as info:
        list(open_watch(Recorder(stream_response(data))))
    assert info.value.code == "internal"


def test_stream_without_end_message_is_unavailable():
    with pytest.raises(ConnectError, match="end-of-stream") as info:
        list(open_watch(Recorder(stream_response(envelope(SAMPLES)))))
    assert info.value.code == "unavailable"


def test_read_timeout_is_reported_as_unavailable():
    def stalls():
        yield envelope(WATCH_HEARTBEAT)
        raise httpx.ReadTimeout("timed out")

    with pytest.raises(ConnectError, match="connection presumed dead") as info:
        list(open_watch(Recorder(stream_response(ChunkStream(stalls))), read_timeout=30))
    assert info.value.code == "unavailable"


def test_tail_decodes_lines_and_heartbeats():
    line = {"_time": "2026-10-21T09:00:00.5Z", "_msg": "hello", "_stream": '{app="x"}'}
    data = envelope({"lineJson": b64json(line), "cursor": line["_time"]}) + envelope({"heartbeat": {}}) + end_stream()
    handler = Recorder(stream_response(data))
    since = datetime.datetime(2026, 10, 21, 8, 0, tzinfo=UTC)
    with tail(config(), "*", cluster_id="c-1", since=since, include_heartbeats=True, http=sync_http(handler)) as stream:
        events = list(stream)
        assert stream.cursor == line["_time"]
    assert [e.kind for e in events] == ["line", "heartbeat"]
    assert events[0].line == line
    assert events[1].cursor == ""
    assert handler.bodies() == [{"clusterId": "c-1", "query": "*", "since": "2026-10-21T08:00:00Z"}]


def test_breaking_out_of_the_loop_closes_the_http_stream():
    def endless():
        while True:
            yield envelope(SAMPLES)

    body = ChunkStream(endless)
    with open_watch(Recorder(stream_response(body))) as stream:
        for n, _ in enumerate(stream):
            if n == 2:
                break
        assert not body.closed
    assert body.closed
    assert list(stream) == []


def test_raw_httpx_client_needs_base_url():
    with pytest.raises(ValueError, match="base_url"):
        watch(config(), "up", http=httpx.Client(transport=httpx.MockTransport(Recorder())))


def test_reconnect_resumes_from_last_cursor_after_unavailable():
    handler = Recorder(
        stream_response(envelope(SAMPLES) + end_stream(error={"code": "unavailable", "message": "server draining"})),
        stream_response(envelope(CHANGE) + end_stream()),
        stream_response(end_stream()),
    )
    stream = open_watch(handler, reconnect=True, reconnect_backoff=0, max_reconnect_attempts=0)
    with stream:
        events = list(stream)
    assert [e.kind for e in events] == ["samples", "change"]
    bodies = handler.bodies()
    assert "cursor" not in bodies[0]
    assert bodies[1]["cursor"] == "v1:1"
    assert bodies[2]["cursor"] == "v1:2"  # a clean end after messages also resumes
    assert stream.reconnects == 2


def test_reconnect_after_connection_breaks():
    def breaks():
        yield envelope(SAMPLES)
        raise httpx.RemoteProtocolError("peer closed connection")

    handler = Recorder(stream_response(ChunkStream(breaks)), stream_response(end_stream()))
    events = list(open_watch(handler, reconnect=True, reconnect_backoff=0, max_reconnect_attempts=0))
    assert [e.kind for e in events] == ["samples"]
    assert handler.bodies()[1]["cursor"] == "v1:1"


def test_reconnect_does_not_retry_non_retryable_codes():
    handler = Recorder(stream_response(end_stream(error={"code": "permission_denied", "message": "no"})))
    with pytest.raises(ConnectError) as info:
        list(open_watch(handler, reconnect=True, reconnect_backoff=0))
    assert info.value.code == "permission_denied"
    assert len(handler.requests) == 1


def test_reconnect_gives_up_after_max_attempts_without_messages():
    unavailable = end_stream(error={"code": "unavailable", "message": "draining"})
    handler = Recorder(*[stream_response(unavailable) for _ in range(4)])
    with pytest.raises(ConnectError) as info:
        list(open_watch(handler, reconnect=True, reconnect_backoff=0, max_reconnect_attempts=3))
    assert info.value.code == "unavailable"
    assert len(handler.requests) == 4


def test_no_reconnect_by_default():
    handler = Recorder(stream_response(end_stream(error={"code": "unavailable", "message": "draining"})))
    with pytest.raises(ConnectError):
        list(open_watch(handler))
    assert len(handler.requests) == 1


def test_cursor_argument_is_the_initial_cursor():
    handler = Recorder(stream_response(end_stream()))
    with open_watch(handler, cursor="v1:9") as stream:
        assert stream.cursor == "v1:9"
        list(stream)
    assert handler.bodies()[0]["cursor"] == "v1:9"


def test_async_watch_parses_split_messages():
    async def run():
        data = envelope(SAMPLES) + envelope(WATCH_HEARTBEAT) + envelope(CHANGE) + end_stream()
        handler = Recorder(stream_response(ChunkStream(odd_chunks(data, (2, 9)))))
        async with awatch(config(), "up", cluster_id="c-1", http=async_http(handler)) as stream:
            events = [e async for e in stream]
            assert stream.cursor == "v1:2"
        return handler, events

    handler, events = asyncio.run(run())
    assert [e.kind for e in events] == ["samples", "change"]
    assert events[0].result == MATRIX
    assert handler.bodies()[0]["clusterId"] == "c-1"
    assert handler.requests[0].headers["authorization"] == "Bearer obs-token"


def test_async_tail_end_stream_error():
    async def run():
        data = envelope({"heartbeat": {}}) + end_stream(error={"code": "resource_exhausted", "message": "lagged"})
        async with atail(config(), "*", cluster_id="c-1", http=async_http(Recorder(stream_response(data)))) as stream:
            return [e async for e in stream]

    with pytest.raises(ConnectError) as info:
        asyncio.run(run())
    assert (info.value.code, info.value.message) == ("resource_exhausted", "lagged")


def test_async_non_200_error():
    async def run():
        response = httpx.Response(403, json={"code": "permission_denied", "message": "missing scope"})
        async with atail(config(), "*", cluster_id="c-1", http=async_http(Recorder(response))) as stream:
            return [e async for e in stream]

    with pytest.raises(ConnectError) as info:
        asyncio.run(run())
    assert (info.value.code, info.value.http_status) == ("permission_denied", 403)


def test_async_breaking_out_closes_the_http_stream():
    def endless():
        while True:
            yield envelope({"heartbeat": {}, "cursor": "v1:1"})

    body = ChunkStream(endless)

    async def run():
        async with awatch(config(), "up", include_heartbeats=True, http=async_http(Recorder(stream_response(body)))) as s:
            n = 0
            async for _ in s:
                n += 1
                if n == 3:
                    break
            assert not body.closed

    asyncio.run(run())
    assert body.closed


def test_async_reconnect_resumes_from_cursor():
    async def run():
        handler = Recorder(
            stream_response(envelope(SAMPLES) + end_stream(error={"code": "unavailable", "message": "draining"})),
            stream_response(end_stream(error={"code": "invalid_argument", "message": "bad"})),
        )
        events = []
        with pytest.raises(ConnectError) as info:
            async with awatch(config(), "up", reconnect=True, reconnect_backoff=0, http=async_http(handler)) as stream:
                async for event in stream:
                    events.append(event)
        return handler, events, info.value

    handler, events, err = asyncio.run(run())
    assert [e.kind for e in events] == ["samples"]
    assert handler.bodies()[1]["cursor"] == "v1:1"
    assert err.code == "invalid_argument"
