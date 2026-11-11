# coding: utf-8

"""
    Decoded results for the Observatory metrics, logs and audit APIs.

    A metrics query returns the Prometheus `data.result` JSON base64-encoded in
    `result.result_json`; log lines and audit events arrive the same way, one
    base64 JSON record per item. This module undoes the base64 and parses the
    JSON, so callers get plain Python values.

    Usage:

        from vpcloud_client.results import decode_result, decode_json_lines

        response = metrics_api.query_org_metrics_range(QueryRangeRequest(...))
        for series in decode_result(response).series():
            print(series.labels, [(s.time, s.value) for s in series.samples])

        lines = decode_json_lines(logs_api.query_logs(cluster_id, request).lines_json)
"""  # noqa: E501

from __future__ import annotations

import base64
import binascii
import datetime
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Iterable, List, NamedTuple, Union

__all__ = (
    "DecodedResult",
    "MalformedResultError",
    "Sample",
    "Series",
    "decode_json_lines",
    "decode_result",
    "decode_result_json",
    "parse_value",
    "to_series",
)


class MalformedResultError(ValueError):
    """A payload that is not base64-encoded JSON of the expected shape."""


@dataclass(frozen=True)
class Sample:
    """One Prometheus sample point.

    Attributes:
        timestamp: Unix seconds, as Prometheus sends it.
        value: the sample value; "NaN", "+Inf" and "-Inf" become float nan/inf.
    """

    timestamp: float
    value: float

    @property
    def time(self) -> datetime.datetime:
        """timestamp as a timezone-aware UTC datetime."""
        return datetime.datetime.fromtimestamp(self.timestamp, tz=datetime.timezone.utc)


@dataclass(frozen=True)
class Series:
    """One labelled series of a vector, matrix or scalar result.

    A vector entry has one sample, a matrix entry one per step, and a scalar
    result is a single series with no labels. Native-histogram points
    (`histogram` / `histograms`) are not samples; read them from `raw`.

    Attributes:
        labels: the series' label set (Prometheus `metric`).
        samples: its float samples, in the order Prometheus sent them.
        raw: the result entry as decoded.
    """

    labels: dict
    samples: tuple
    raw: Any = field(default=None, repr=False, compare=False)


class DecodedResult(NamedTuple):
    """A decoded metrics result; unpacks as `result_type, result`.

    Attributes:
        result_type: "vector", "matrix", "scalar" or "string"; "" when the
            response carried no result.
        result: the Prometheus `data.result` JSON as Python values: a list of
            {"metric", "value"} (vector) or {"metric", "values"} (matrix)
            entries, or one [t, "v"] pair (scalar, string). [] when absent.
    """

    result_type: str
    result: List[Any]

    def series(self) -> List[Series]:
        """The result as typed Series; see to_series()."""
        return to_series(self.result_type, self.result)


def decode_result(source: Any) -> DecodedResult:
    """Decode a metrics query's result.

    source may be the response of query_metrics, query_metrics_range,
    query_org_metrics or query_org_metrics_range, its `result`, the ApiResponse
    of a `*_with_http_info` call, a JSON dict of any of those, or None. A
    missing result decodes to DecodedResult("", []).

    Raises:
        MalformedResultError: result_json is not base64 of a JSON array.
        TypeError: source is none of the above.
    """
    if source is None:
        return DecodedResult("", [])
    if hasattr(source, "status_code") and hasattr(source, "data"):
        return decode_result(source.data)
    if isinstance(source, Mapping):
        if "result" in source:
            return decode_result(source["result"])
        result_type = source.get("resultType", source.get("result_type"))
        result_json = source.get("resultJson", source.get("result_json"))
    elif hasattr(source, "result_json"):
        result_type, result_json = source.result_type, source.result_json
    elif hasattr(source, "result"):
        return decode_result(source.result)
    else:
        raise TypeError(f"expected a metrics query response or its result, got {type(source).__name__}")
    result_type = "" if result_type is None else str(result_type)
    if result_json is None:
        return DecodedResult(result_type, [])
    return DecodedResult(result_type, decode_result_json(result_json))


def decode_result_json(value: Union[str, bytes]) -> List[Any]:
    """Decode a `result_json` value: base64 text, or bytes holding either that
    base64 or the JSON itself.

    Raises:
        MalformedResultError: not base64, not JSON, or not a JSON array.
    """
    result = _decode_json_bytes(value)
    if not isinstance(result, list):
        raise MalformedResultError(f"result_json is not a JSON array (got {type(result).__name__})")
    return result


def decode_json_lines(values: Union[Iterable[Union[str, bytes]], None]) -> List[Any]:
    """Decode log lines (`lines_json`) or audit events (`events_json`): each
    item is the base64 of one JSON record. An item that is not JSON is
    returned as text rather than raising."""
    if values is None:
        return []
    return [_decode_json_bytes(v, lenient=True) for v in values]


def to_series(result_type: str, result: List[Any]) -> List[Series]:
    """Convert a decoded result into Series.

    Raises:
        ValueError: a "string" result, which has no numeric samples.
        MalformedResultError: an entry that does not have Prometheus' shape.
    """
    if not result:
        return []
    if result_type == "string":
        raise ValueError("a string result has no numeric samples; read DecodedResult.result")
    if result_type == "scalar":
        return [Series(labels={}, samples=(_sample(result),), raw=result)]
    series = []
    for entry in result:
        if not isinstance(entry, Mapping):
            raise MalformedResultError(f"result entry is not an object: {entry!r:.100}")
        labels = entry.get("metric") or {}
        if "value" in entry:
            samples = (_sample(entry["value"]),)
        else:
            samples = tuple(_sample(point) for point in entry.get("values") or [])
        series.append(Series(labels=dict(labels), samples=samples, raw=entry))
    return series


def parse_value(value: Union[str, float, int]) -> float:
    """Parse a Prometheus sample value ("1.5", "NaN", "+Inf", "-Inf")."""
    try:
        return float(value)
    except (TypeError, ValueError) as e:
        raise MalformedResultError(f"invalid sample value: {value!r:.100}") from e


def _sample(point: Any) -> Sample:
    if not isinstance(point, (list, tuple)) or len(point) != 2:
        raise MalformedResultError(f"sample is not a [timestamp, value] pair: {point!r:.100}")
    try:
        timestamp = float(point[0])
    except (TypeError, ValueError) as e:
        raise MalformedResultError(f"invalid sample timestamp: {point[0]!r:.100}") from e
    return Sample(timestamp=timestamp, value=parse_value(point[1]))


def _payload_bytes(value: Any) -> bytes:
    """Undo the base64 of a bytes field. Bytes that already start like JSON
    pass through: "[" and "{" are not in the base64 alphabet."""
    if isinstance(value, (bytes, bytearray, memoryview)):
        raw = bytes(value)
        if raw.lstrip()[:1] in (b"[", b"{"):
            return raw
    elif not isinstance(value, str):
        raise MalformedResultError(f"expected base64 str or bytes, got {type(value).__name__}")
    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as e:
        raise MalformedResultError(f"not valid base64: {e}") from e


def _decode_json_bytes(value: Any, *, lenient: bool = False) -> Any:
    """Decode a bytes field that holds JSON. lenient returns a payload that is
    not JSON as text (log lines) instead of raising."""
    raw = _payload_bytes(value)
    try:
        return json.loads(raw)
    except ValueError as e:
        if lenient:
            return raw.decode("utf-8", errors="replace")
        raise MalformedResultError(f"not valid JSON: {e}") from e
