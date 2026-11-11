# coding: utf-8

"""
    Live metrics (Watch) and log (Tail) streams from the Observatory APIs.

    Watch re-evaluates PromQL every step and pushes what is new; Tail pushes
    log lines as they arrive. Both are long-lived server streams, which the
    generated REST methods can't hold open, so this module speaks the Connect
    protocol (https://connectrpc.com/docs/protocol) over httpx: HTTP/1.1, JSON,
    no compression. Requests go to `Configuration.observatory_host` with the
    same Observatory token as the other Observatory methods.

    Usage:

        import vpcloud_client
        from vpcloud_client.streaming import watch

        config = vpcloud_client.Configuration()  # VPCLOUD_CLIENT_ID / VPCLOUD_CLIENT_SECRET
        with watch(config, "sum(rate(node_cpu_seconds_total[5m]))", step="30s", reconnect=True) as stream:
            for event in stream:
                for series in event.series():
                    print(series.labels, [(s.time, s.value) for s in series.samples])

    Iterate inside `with` (or `async with` for awatch/atail): leaving the
    block, for example with `break`, closes the HTTP stream.
"""  # noqa: E501

from __future__ import annotations

import asyncio
import datetime
import json
import random
import re
import struct
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, AsyncIterator, Callable, Dict, Generator, Generic, Iterator, List, Optional, Tuple, TypeVar, Union

import httpx

from vpcloud_client.results import Series, _decode_json_bytes, to_series

__all__ = (
    "DEFAULT_CONNECT_TIMEOUT",
    "DEFAULT_READ_TIMEOUT",
    "AsyncServerStream",
    "ConnectError",
    "ServerStream",
    "TailEvent",
    "WatchEvent",
    "atail",
    "awatch",
    "tail",
    "watch",
)

WATCH_PROCEDURE = "/observatory.v1.MetricsService/Watch"
TAIL_PROCEDURE = "/observatory.v1.LogsService/Tail"

DEFAULT_READ_TIMEOUT = 60.0
"""Seconds without any bytes from the server before the stream is presumed
dead. The server sends a heartbeat about every 15s, so this only trips on a
broken connection."""

DEFAULT_CONNECT_TIMEOUT = 10.0
"""Seconds allowed to connect and send the request."""

DEFAULT_RECONNECT_BACKOFF = 0.5
"""Initial delay between reconnect attempts; doubles up to MAX_RECONNECT_BACKOFF."""

MAX_RECONNECT_BACKOFF = 30.0

MAX_MESSAGE_BYTES = 64 << 20
"""Largest single stream message accepted. Guards against reading a non-Connect
body (for example a proxy's HTML page) as a gigantic length prefix."""

RECONNECT_CODES = frozenset({"unavailable"})
"""Connect codes after which reconnect=True resumes from the last cursor. The
server ends a stream with unavailable when a replica drains; broken
connections and read timeouts surface as unavailable too."""

WATCH_MODES = {"samples": "WATCH_MODE_SAMPLES", "changes": "WATCH_MODE_CHANGES"}

_FLAG_COMPRESSED = 0x01
_FLAG_END_STREAM = 0x02
_ENVELOPE = struct.Struct(">BI")

# Connect's mapping for HTTP statuses that arrive without a Connect error body.
_HTTP_STATUS_CODES = {
    400: "internal",
    401: "unauthenticated",
    403: "permission_denied",
    404: "unimplemented",
    429: "unavailable",
    502: "unavailable",
    503: "unavailable",
    504: "unavailable",
}


class ConnectError(Exception):
    """A stream error, from the server or from a broken connection.

    Attributes:
        code: the Connect code as sent, for example "unauthenticated",
            "permission_denied", "invalid_argument", "resource_exhausted" or
            "unavailable". See https://connectrpc.com/docs/protocol#error-codes.
        message: the server's error message.
        details: the error's `details` list as sent.
        metadata: trailers from the end-of-stream message, if any.
        http_status: the HTTP status when the error came from a non-200
            response; None for errors sent on the stream itself.
    """

    def __init__(
        self,
        code: str,
        message: str = "",
        *,
        details: Optional[List[Any]] = None,
        metadata: Optional[Mapping[str, List[str]]] = None,
        http_status: Optional[int] = None,
    ) -> None:
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message
        self.details = details or []
        self.metadata = dict(metadata or {})
        self.http_status = http_status


@dataclass(frozen=True)
class WatchEvent:
    """One Watch message.

    kind is "samples", "change", "heartbeat", or "unknown" (an event type newer
    than this SDK; inspect `raw`).

    Attributes:
        kind: which event this is.
        cursor: resume token covering everything sent so far. Pass it as
            `cursor=` to resume.
        name: the query the event belongs to (samples and change).
        result_type: Prometheus resultType, normally "matrix" (samples).
        result: the decoded Prometheus `data.result` list (samples).
        time: evaluation time of the change (change).
        appeared: series that started matching, as Prometheus vector entries
            {"metric": {...}, "value": [t, "v"]} (change).
        disappeared: label sets of series that stopped matching (change).
        raw: the message as received.
    """

    kind: str
    cursor: str
    name: str = ""
    result_type: str = ""
    result: Any = None
    time: Optional[datetime.datetime] = None
    appeared: List[Any] = field(default_factory=list)
    disappeared: List[Any] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def is_heartbeat(self) -> bool:
        return self.kind == "heartbeat"

    def series(self) -> List[Series]:
        """A samples event's result as typed Series (see results.to_series);
        [] for other events."""
        if self.kind != "samples" or not self.result:
            return []
        return to_series(self.result_type, self.result)


@dataclass(frozen=True)
class TailEvent:
    """One Tail message.

    Attributes:
        kind: "line", "heartbeat", or "unknown" (inspect `raw`).
        cursor: the line's `_time`, used to resume. Empty on heartbeats.
        line: the decoded log line, normally a dict of fields (`_time`,
            `_msg`, `_stream`, ...).
        raw: the message as received.
    """

    kind: str
    cursor: str
    line: Any = None
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def is_heartbeat(self) -> bool:
        return self.kind == "heartbeat"


E = TypeVar("E", WatchEvent, TailEvent)
Queries = Union[str, List[str], Mapping[str, str]]


def watch(
    client: Any,
    queries: Queries,
    *,
    cluster_id: str = "",
    step: Union[str, float, None] = None,
    mode: str = "samples",
    cursor: str = "",
    include_heartbeats: bool = False,
    reconnect: bool = False,
    max_reconnect_attempts: int = 5,
    reconnect_backoff: float = DEFAULT_RECONNECT_BACKOFF,
    read_timeout: Optional[float] = DEFAULT_READ_TIMEOUT,
    connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
    headers: Optional[Mapping[str, str]] = None,
    http: Optional[httpx.Client] = None,
) -> ServerStream[WatchEvent]:
    """Open a Watch stream. Iterate the result to receive WatchEvents.

    Args:
        client: a `vpcloud_client.ApiClient` or `Configuration`. The stream
            goes to its `observatory_host` with an Observatory token.
        queries: one PromQL string, a list of them (named "q0", "q1", ...), or
            a {name: query} mapping. Each event carries its query's name.
        cluster_id: watch one cluster; omit to watch the whole organization.
        step: evaluation interval, as a duration string ("30s") or seconds.
            Omit for the server's default.
        mode: "samples" (every new point) or "changes" (series appearing and
            disappearing).
        cursor: resume from this cursor, for example a previous
            `stream.cursor`.
        include_heartbeats: also yield heartbeat events (skipped by default).
        reconnect: resume from the last cursor when the stream ends at its
            maximum lifetime, the server drains, or the connection breaks.
        max_reconnect_attempts: consecutive reconnects that deliver nothing
            before the last error is raised.
        reconnect_backoff: initial delay between reconnects, in seconds.
        read_timeout: seconds with no bytes before the connection is presumed
            dead (raises ConnectError("unavailable")). None waits forever.
        connect_timeout: seconds to connect and send the request.
        headers: extra request headers.
        http: an httpx.Client to send with (for a proxy or custom TLS); its
            base_url must be the Observatory host. By default one is created
            from the configuration and closed with the stream.

    The connection opens on first iteration, so errors such as
    ConnectError("permission_denied") are raised from the loop.
    """
    config = _configuration(client)
    request = _watch_request(queries, cluster_id, step, mode, cursor)
    options = _Options(include_heartbeats, read_timeout, connect_timeout, headers, reconnect,
                       max_reconnect_attempts, reconnect_backoff, _token_source(config))
    return ServerStream(*_sync_http(config, http), WATCH_PROCEDURE, request, _decode_watch, options)


def tail(
    client: Any,
    query: str,
    *,
    cluster_id: str,
    since: Optional[datetime.datetime] = None,
    cursor: str = "",
    include_heartbeats: bool = False,
    reconnect: bool = False,
    max_reconnect_attempts: int = 5,
    reconnect_backoff: float = DEFAULT_RECONNECT_BACKOFF,
    read_timeout: Optional[float] = DEFAULT_READ_TIMEOUT,
    connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
    headers: Optional[Mapping[str, str]] = None,
    http: Optional[httpx.Client] = None,
) -> ServerStream[TailEvent]:
    """Open a Tail stream of one cluster's logs. Iterate the result to receive
    TailEvents.

    Args:
        query: LogsQL, sent as written.
        cluster_id: the cluster whose logs to tail.
        since: start from this time (timezone-aware) rather than now.
        cursor: resume after this cursor, for example a previous `stream.cursor`.

    The other arguments are as for `watch`. A resumed tail starts at the
    cursor's timestamp, so lines sharing it may be delivered again; dedupe on
    `_time` + `_stream_id` if that matters.
    """
    config = _configuration(client)
    request = _tail_request(query, cluster_id, since, cursor)
    options = _Options(include_heartbeats, read_timeout, connect_timeout, headers, reconnect,
                       max_reconnect_attempts, reconnect_backoff, _token_source(config))
    return ServerStream(*_sync_http(config, http), TAIL_PROCEDURE, request, _decode_tail, options)


def awatch(
    client: Any,
    queries: Queries,
    *,
    cluster_id: str = "",
    step: Union[str, float, None] = None,
    mode: str = "samples",
    cursor: str = "",
    include_heartbeats: bool = False,
    reconnect: bool = False,
    max_reconnect_attempts: int = 5,
    reconnect_backoff: float = DEFAULT_RECONNECT_BACKOFF,
    read_timeout: Optional[float] = DEFAULT_READ_TIMEOUT,
    connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
    headers: Optional[Mapping[str, str]] = None,
    http: Optional[httpx.AsyncClient] = None,
) -> AsyncServerStream[WatchEvent]:
    """Async `watch`, with the same arguments (`http` is an httpx.AsyncClient).
    Use `async with awatch(...) as stream: async for event in stream: ...`."""
    config = _configuration(client)
    request = _watch_request(queries, cluster_id, step, mode, cursor)
    options = _Options(include_heartbeats, read_timeout, connect_timeout, headers, reconnect,
                       max_reconnect_attempts, reconnect_backoff, _token_source(config))
    return AsyncServerStream(*_async_http(config, http), WATCH_PROCEDURE, request, _decode_watch, options)


def atail(
    client: Any,
    query: str,
    *,
    cluster_id: str,
    since: Optional[datetime.datetime] = None,
    cursor: str = "",
    include_heartbeats: bool = False,
    reconnect: bool = False,
    max_reconnect_attempts: int = 5,
    reconnect_backoff: float = DEFAULT_RECONNECT_BACKOFF,
    read_timeout: Optional[float] = DEFAULT_READ_TIMEOUT,
    connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
    headers: Optional[Mapping[str, str]] = None,
    http: Optional[httpx.AsyncClient] = None,
) -> AsyncServerStream[TailEvent]:
    """Async `tail`, with the same arguments (`http` is an httpx.AsyncClient)."""
    config = _configuration(client)
    request = _tail_request(query, cluster_id, since, cursor)
    options = _Options(include_heartbeats, read_timeout, connect_timeout, headers, reconnect,
                       max_reconnect_attempts, reconnect_backoff, _token_source(config))
    return AsyncServerStream(*_async_http(config, http), TAIL_PROCEDURE, request, _decode_tail, options)


def _watch_request(queries: Queries, cluster_id: str, step: Union[str, float, None], mode: str, cursor: str) -> Dict[str, Any]:
    if mode not in WATCH_MODES:
        raise ValueError(f"mode must be one of {sorted(WATCH_MODES)}, got {mode!r}")
    request: Dict[str, Any] = {"queries": _watch_queries(queries), "mode": WATCH_MODES[mode]}
    if cluster_id:
        request["clusterId"] = cluster_id
    if step is not None:
        request["step"] = _duration(step)
    if cursor:
        request["cursor"] = cursor
    return request


def _tail_request(query: str, cluster_id: str, since: Optional[datetime.datetime], cursor: str) -> Dict[str, Any]:
    if not cluster_id:
        raise ValueError("tail needs a cluster_id")
    request: Dict[str, Any] = {"clusterId": cluster_id, "query": query}
    if since is not None:
        request["since"] = _rfc3339(since)
    if cursor:
        request["cursor"] = cursor
    return request


@dataclass(frozen=True)
class _Options:
    include_heartbeats: bool
    read_timeout: Optional[float]
    connect_timeout: float
    headers: Optional[Mapping[str, str]]
    reconnect: bool
    max_reconnect_attempts: int
    reconnect_backoff: float
    token: Callable[[], str]

    def timeout(self) -> httpx.Timeout:
        # httpx timeouts are per operation, never a total, so a long-lived
        # stream is only cut when no bytes arrive for read_timeout.
        return httpx.Timeout(
            connect=self.connect_timeout,
            read=self.read_timeout,
            write=self.connect_timeout,
            pool=self.connect_timeout,
        )

    def request_headers(self) -> Dict[str, str]:
        out = dict(self.headers or {})
        out.update(
            {
                "Content-Type": "application/connect+json",
                "Connect-Protocol-Version": "1",
                # No Connect-Accept-Encoding, so the server sends uncompressed
                # messages; identity keeps any HTTP-level gzip off the stream.
                "Accept-Encoding": "identity",
                # Fetched per connect, so a reconnect gets a fresh token.
                "Authorization": self.token(),
            }
        )
        return out


class _Stream(Generic[E]):
    """State and protocol handling shared by the sync and async streams."""

    def __init__(self, procedure: str, request: Dict[str, Any], decode: Callable[[Dict[str, Any]], E], options: _Options) -> None:
        self._procedure = procedure
        self._request = request
        self._decode = decode
        self._options = options
        self.cursor: str = str(request.get("cursor") or "")
        """Last non-empty cursor received (or the one the stream started from).
        Pass it as `cursor=` to resume."""
        self.response_headers: Optional[httpx.Headers] = None
        """Headers of the most recent HTTP response."""
        self.trailers: Dict[str, List[str]] = {}
        """Metadata from the most recent end-of-stream message."""
        self.reconnects = 0
        """How many times this stream has reconnected."""
        self._closed = False

    def _body(self) -> bytes:
        request = dict(self._request)
        if self.cursor:
            request["cursor"] = self.cursor
        return _envelope(json.dumps(request).encode())

    def _check_head(self, response: httpx.Response) -> None:
        self.response_headers = response.headers
        content_type = response.headers.get("content-type", "")
        if response.status_code == 200 and content_type.startswith("application/connect+json"):
            return
        if response.status_code == 200:
            raise ConnectError(
                "unknown",
                f"unexpected content-type {content_type!r}; is observatory_host the Observatory API root?",
                http_status=200,
            )
        raise _http_error(response)

    def _messages(self, parser: _EnvelopeParser, chunk: bytes) -> Iterator[E]:
        """Decode the complete messages in chunk; raise on end-of-stream errors."""
        for flags, payload in parser.feed(chunk):
            if flags & _FLAG_COMPRESSED:
                raise ConnectError("internal", "server sent a compressed message, but this client does not accept compression")
            if flags & _FLAG_END_STREAM:
                parser.ended = True
                self._end_stream(payload)
                return
            event = self._decode(_json(payload))
            if event.cursor:
                self.cursor = event.cursor
            yield event

    def _end_stream(self, payload: bytes) -> None:
        end = _json(payload) if payload else {}
        self.trailers = {k: list(v) for k, v in (end.get("metadata") or {}).items()}
        err = end.get("error")
        if err:
            raise ConnectError(
                str(err.get("code") or "unknown"),
                str(err.get("message") or ""),
                details=err.get("details"),
                metadata=self.trailers,
            )

    def _visible(self, event: E) -> bool:
        return self._options.include_heartbeats or not event.is_heartbeat

    def _after_attempt(self, received: bool, failures: int, err: Optional[ConnectError]) -> Tuple[int, Optional[float]]:
        """Decide what follows one attempt; returns (failures, delay) or raises.
        A delay of None means stop iterating cleanly."""
        opts = self._options
        if not opts.reconnect or self._closed:
            if err is not None:
                raise err
            return failures, None
        if err is not None and err.code not in RECONNECT_CODES:
            raise err
        if received:
            # The stream delivered something (for example, it ran to its
            # maximum lifetime): resume straight away.
            return 0, 0.0
        failures += 1
        if failures > opts.max_reconnect_attempts:
            if err is not None:
                raise err
            return failures, None
        delay = min(MAX_RECONNECT_BACKOFF, opts.reconnect_backoff * 2 ** (failures - 1))
        return failures, delay * (0.5 + random.random() / 2)


class ServerStream(_Stream[E]):
    """A server stream; iterate it for events. Use it as a context manager so
    leaving the loop early closes the HTTP connection."""

    def __init__(self, http: httpx.Client, owns_http: bool, procedure: str, request: Dict[str, Any],
                 decode: Callable[[Dict[str, Any]], E], options: _Options) -> None:
        super().__init__(procedure, request, decode, options)
        self._http = http
        self._owns_http = owns_http
        self._response: Optional[httpx.Response] = None
        self._events: Optional[Generator[E, None, None]] = None

    def __enter__(self) -> "ServerStream[E]":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def __iter__(self) -> "ServerStream[E]":
        return self

    def __next__(self) -> E:
        if self._events is None:
            if self._closed:
                raise StopIteration
            self._events = self._run()
        return next(self._events)

    def close(self) -> None:
        """Close the HTTP stream. Safe to call more than once."""
        self._closed = True
        if self._events is not None:
            self._events.close()
        if self._response is not None:
            self._response.close()
            self._response = None
        if self._owns_http:
            self._http.close()

    def _run(self) -> Generator[E, None, None]:
        failures = 0
        while True:
            received = False
            err: Optional[ConnectError] = None
            try:
                for event in self._attempt():
                    received = True
                    if self._visible(event):
                        yield event
            except ConnectError as e:
                err = e
            failures, delay = self._after_attempt(received, failures, err)
            if delay is None:
                return
            time.sleep(delay)
            self.reconnects += 1

    def _attempt(self) -> Iterator[E]:
        request = self._http.build_request(
            "POST", self._procedure, content=self._body(),
            headers=self._options.request_headers(), timeout=self._options.timeout(),
        )
        try:
            response = self._http.send(request, stream=True)
        except httpx.TransportError as e:
            raise _transport_error(e, self._options) from e
        self._response = response
        try:
            if response.status_code != 200:
                response.read()
            self._check_head(response)
            parser = _EnvelopeParser()
            for chunk in response.iter_bytes():
                yield from self._messages(parser, chunk)
                if parser.ended:
                    return
            parser.finish()
        except httpx.TransportError as e:
            raise _transport_error(e, self._options) from e
        finally:
            response.close()
            self._response = None


class AsyncServerStream(_Stream[E]):
    """Async server stream; use `async with` and `async for`."""

    def __init__(self, http: httpx.AsyncClient, owns_http: bool, procedure: str, request: Dict[str, Any],
                 decode: Callable[[Dict[str, Any]], E], options: _Options) -> None:
        super().__init__(procedure, request, decode, options)
        self._http = http
        self._owns_http = owns_http
        self._response: Optional[httpx.Response] = None
        self._events: Optional[AsyncGenerator[E, None]] = None

    async def __aenter__(self) -> "AsyncServerStream[E]":
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()

    def __aiter__(self) -> "AsyncServerStream[E]":
        return self

    async def __anext__(self) -> E:
        if self._events is None:
            if self._closed:
                raise StopAsyncIteration
            self._events = self._run()
        return await self._events.__anext__()

    async def aclose(self) -> None:
        """Close the HTTP stream. Safe to call more than once."""
        self._closed = True
        if self._events is not None:
            await self._events.aclose()
        if self._response is not None:
            await self._response.aclose()
            self._response = None
        if self._owns_http:
            await self._http.aclose()

    async def _run(self) -> AsyncGenerator[E, None]:
        failures = 0
        while True:
            received = False
            err: Optional[ConnectError] = None
            try:
                async for event in self._attempt():
                    received = True
                    if self._visible(event):
                        yield event
            except ConnectError as e:
                err = e
            failures, delay = self._after_attempt(received, failures, err)
            if delay is None:
                return
            await asyncio.sleep(delay)
            self.reconnects += 1

    async def _attempt(self) -> AsyncIterator[E]:
        request = self._http.build_request(
            "POST", self._procedure, content=self._body(),
            headers=self._options.request_headers(), timeout=self._options.timeout(),
        )
        try:
            response = await self._http.send(request, stream=True)
        except httpx.TransportError as e:
            raise _transport_error(e, self._options) from e
        self._response = response
        try:
            if response.status_code != 200:
                await response.aread()
            self._check_head(response)
            parser = _EnvelopeParser()
            async for chunk in response.aiter_bytes():
                for event in self._messages(parser, chunk):
                    yield event
                if parser.ended:
                    return
            parser.finish()
        except httpx.TransportError as e:
            raise _transport_error(e, self._options) from e
        finally:
            await response.aclose()
            self._response = None


class _EnvelopeParser:
    """Splits a byte stream into Connect envelopes (flags, payload)."""

    def __init__(self) -> None:
        self._buf = bytearray()
        self.ended = False

    def feed(self, chunk: bytes) -> Iterator[Tuple[int, bytes]]:
        self._buf.extend(chunk)
        while len(self._buf) >= _ENVELOPE.size:
            flags, length = _ENVELOPE.unpack_from(self._buf)
            if length > MAX_MESSAGE_BYTES:
                raise ConnectError("resource_exhausted", f"stream message of {length} bytes exceeds the {MAX_MESSAGE_BYTES}-byte limit")
            end = _ENVELOPE.size + length
            if len(self._buf) < end:
                return
            payload = bytes(self._buf[_ENVELOPE.size:end])
            del self._buf[:end]
            yield flags, payload

    def finish(self) -> None:
        """Raise for a body that ended without an end-of-stream message."""
        if not self.ended:
            raise ConnectError("unavailable", "stream ended without an end-of-stream message")


def _configuration(client: Any) -> Any:
    from vpcloud_client.api_client import ApiClient
    from vpcloud_client.configuration import Configuration

    if isinstance(client, ApiClient):
        return client.configuration
    if isinstance(client, Configuration):
        return client
    raise TypeError(f"expected a vpcloud_client ApiClient or Configuration, got {type(client).__name__}")


def _token_source(config: Any) -> Callable[[], str]:
    """The Authorization value for Observatory, resolved per connect. Raises
    AuthenticationError without Observatory credentials: the Harbor token is
    never sent to observatory_host."""
    def token() -> str:
        return config.auth_settings(service="observatory")["bearerAuth"]["value"]
    return token


def _verify(config: Any) -> Any:
    if not config.verify_ssl:
        return False
    return config.ssl_ca_cert or True


def _sync_http(config: Any, http: Optional[httpx.Client]) -> Tuple[httpx.Client, bool]:
    if http is not None:
        _require_base_url(http)
        return http, False
    return httpx.Client(base_url=config.observatory_host, verify=_verify(config)), True


def _async_http(config: Any, http: Optional[httpx.AsyncClient]) -> Tuple[httpx.AsyncClient, bool]:
    if http is not None:
        _require_base_url(http)
        return http, False
    return httpx.AsyncClient(base_url=config.observatory_host, verify=_verify(config)), True


def _require_base_url(http: Any) -> None:
    if not http.base_url.host:
        raise ValueError("the httpx client needs base_url set to the Observatory host, e.g. https://observatory.voltagepark.com")


def _watch_queries(queries: Queries) -> List[Dict[str, str]]:
    if isinstance(queries, str):
        return [{"name": "q0", "query": queries}]
    if isinstance(queries, Mapping):
        pairs = list(queries.items())
    else:
        pairs = [(f"q{i}", q) for i, q in enumerate(queries)]
    if not pairs:
        raise ValueError("watch needs at least one query")
    return [{"name": str(name), "query": str(query)} for name, query in pairs]


def _duration(step: Union[str, float]) -> str:
    if isinstance(step, (int, float)):
        return f"{float(step):g}s"
    return str(step)


def _rfc3339(value: datetime.datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("since must be timezone-aware, e.g. datetime.datetime.now(datetime.timezone.utc)")
    return value.astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def _envelope(payload: bytes) -> bytes:
    return _ENVELOPE.pack(0, len(payload)) + payload


def _json(payload: bytes) -> Dict[str, Any]:
    try:
        value = json.loads(payload)
    except ValueError as e:
        raise ConnectError("internal", f"invalid JSON in stream message: {e}") from e
    if not isinstance(value, dict):
        raise ConnectError("internal", "stream message is not a JSON object")
    return value


def _http_error(response: httpx.Response) -> ConnectError:
    status = response.status_code
    body: Any = None
    try:
        body = response.json()
    except ValueError:
        pass
    if isinstance(body, dict) and body.get("code"):
        return ConnectError(str(body["code"]), str(body.get("message") or ""), details=body.get("details"), http_status=status)
    text = response.text.strip()[:300]
    return ConnectError(_HTTP_STATUS_CODES.get(status, "unknown"), text or f"HTTP {status}", http_status=status)


def _transport_error(err: httpx.TransportError, options: _Options) -> ConnectError:
    if isinstance(err, httpx.ReadTimeout):
        return ConnectError(
            "unavailable",
            f"no data from the server for {options.read_timeout}s (heartbeats are about every 15s); connection presumed dead",
        )
    return ConnectError("unavailable", f"httpx.{type(err).__name__}: {err}")


def _field(message: Mapping[str, Any], camel: str, snake: str) -> Any:
    return message[camel] if camel in message else message.get(snake)


def _bytes_json(value: Any) -> Any:
    return None if value is None else _decode_json_bytes(value, lenient=True)


_FRACTION = re.compile(r"\.(\d{6})\d+")


def _timestamp(value: Any) -> Optional[datetime.datetime]:
    if not value:
        return None
    # Timestamps carry up to nanoseconds; datetime holds microseconds.
    text = _FRACTION.sub(r".\1", str(value)).replace("Z", "+00:00")
    return datetime.datetime.fromisoformat(text)


def _decode_watch(message: Dict[str, Any]) -> WatchEvent:
    cursor = str(message.get("cursor") or "")
    if "heartbeat" in message:
        return WatchEvent(kind="heartbeat", cursor=cursor, raw=message)
    samples = message.get("samples")
    if samples is not None:
        result = samples.get("result") or {}
        return WatchEvent(
            kind="samples",
            cursor=cursor,
            name=str(samples.get("name") or ""),
            result_type=str(_field(result, "resultType", "result_type") or ""),
            result=_bytes_json(_field(result, "resultJson", "result_json")),
            raw=message,
        )
    change = message.get("change")
    if change is not None:
        return WatchEvent(
            kind="change",
            cursor=cursor,
            name=str(change.get("name") or ""),
            time=_timestamp(change.get("time")),
            appeared=[_bytes_json(v) for v in _field(change, "appearedJson", "appeared_json") or []],
            disappeared=[_bytes_json(v) for v in _field(change, "disappearedJson", "disappeared_json") or []],
            raw=message,
        )
    return WatchEvent(kind="unknown", cursor=cursor, raw=message)


def _decode_tail(message: Dict[str, Any]) -> TailEvent:
    cursor = str(message.get("cursor") or "")
    if "heartbeat" in message:
        return TailEvent(kind="heartbeat", cursor=cursor, raw=message)
    line = _field(message, "lineJson", "line_json")
    if line is not None:
        return TailEvent(kind="line", cursor=cursor, line=_bytes_json(line), raw=message)
    return TailEvent(kind="unknown", cursor=cursor, raw=message)
