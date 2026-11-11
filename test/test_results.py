# coding: utf-8

"""Tests for vpcloud_client.results. No network."""

import base64
import datetime
import json
import math

import pytest

from vpcloud_client.api_response import ApiResponse
from vpcloud_client.models.observatory_v1_metrics_result import ObservatoryV1MetricsResult
from vpcloud_client.models.observatory_v1_query_range_response import ObservatoryV1QueryRangeResponse
from vpcloud_client.models.observatory_v1_query_response import ObservatoryV1QueryResponse
from vpcloud_client.results import (
    DecodedResult,
    MalformedResultError,
    Sample,
    Series,
    decode_json_lines,
    decode_result,
    decode_result_json,
    parse_value,
    to_series,
)

VECTOR = [
    {"metric": {"__name__": "up", "job": "node"}, "value": [1730822400.123, "1"]},
    {"metric": {"__name__": "up", "job": "dcgm"}, "value": [1730822400.123, "0"]},
]
MATRIX = [
    {"metric": {"gpu": "0"}, "values": [[1730822400, "41.5"], [1730822415, "42"]]},
]


def b64(value):
    return base64.b64encode(json.dumps(value).encode()).decode()


def test_vector_from_query_response():
    response = ObservatoryV1QueryResponse.from_dict({"result": {"resultType": "vector", "resultJson": b64(VECTOR)}})

    decoded = decode_result(response)

    assert decoded == DecodedResult("vector", VECTOR)
    result_type, result = decoded
    assert result_type == "vector" and result == VECTOR
    series = decoded.series()
    assert [s.labels for s in series] == [VECTOR[0]["metric"], VECTOR[1]["metric"]]
    assert series[0].samples == (Sample(1730822400.123, 1.0),)
    assert series[0].samples[0].time == datetime.datetime(
        2024, 11, 5, 16, 0, 0, 123000, tzinfo=datetime.timezone.utc
    )


def test_matrix_from_query_range_response():
    response = ObservatoryV1QueryRangeResponse.from_dict({"result": {"resultType": "matrix", "resultJson": b64(MATRIX)}})

    decoded = decode_result(response)

    assert decoded.result_type == "matrix"
    assert decoded.result == MATRIX
    assert decoded.series() == [
        Series(labels={"gpu": "0"}, samples=(Sample(1730822400.0, 41.5), Sample(1730822415.0, 42.0)))
    ]


def test_scalar_and_string():
    scalar = decode_result(ObservatoryV1MetricsResult(result_type="scalar", result_json=b64([1730822400, "3"])))
    assert scalar.result == [1730822400, "3"]
    assert scalar.series() == [Series(labels={}, samples=(Sample(1730822400.0, 3.0),))]

    string = decode_result(ObservatoryV1MetricsResult(result_type="string", result_json=b64([1730822400, "hello"])))
    assert string.result == [1730822400, "hello"]
    with pytest.raises(ValueError, match="string result"):
        string.series()


@pytest.mark.parametrize(
    "source",
    [
        None,
        ObservatoryV1QueryResponse(),
        ObservatoryV1QueryResponse.from_dict({"result": {}}),
        ObservatoryV1MetricsResult(result_type="vector"),
        {"result": {"resultType": "vector"}},
    ],
)
def test_empty_or_absent_result_is_empty_list(source):
    decoded = decode_result(source)
    assert decoded.result == []
    assert decoded.series() == []


def test_bytes_and_str_payloads_decode_alike():
    text = b64(VECTOR)
    assert decode_result_json(text) == VECTOR
    assert decode_result_json(text.encode()) == VECTOR
    assert decode_result_json(json.dumps(VECTOR).encode()) == VECTOR
    assert decode_result_json(bytearray(b'  [{"metric": {}, "value": [1, "2"]}]')) == [{"metric": {}, "value": [1, "2"]}]


def test_json_dicts_and_api_response():
    assert decode_result({"resultType": "vector", "resultJson": b64(VECTOR)}).result == VECTOR
    assert decode_result({"result_type": "matrix", "result_json": b64(MATRIX)}).result_type == "matrix"
    assert decode_result({"result": {"resultType": "vector", "resultJson": b64(VECTOR)}}).result == VECTOR

    data = ObservatoryV1QueryResponse.from_dict({"result": {"resultType": "vector", "resultJson": b64(VECTOR)}})
    response = ApiResponse(status_code=200, headers={}, data=data, raw_data=b"")
    assert decode_result(response).result == VECTOR


def test_special_float_values():
    assert math.isnan(parse_value("NaN"))
    assert parse_value("+Inf") == math.inf
    assert parse_value("-Inf") == -math.inf
    assert parse_value("1e3") == 1000.0
    assert parse_value(2) == 2.0

    result = [{"metric": {}, "values": [[1, "NaN"], [2, "+Inf"], [3, "-Inf"]]}]
    (series,) = to_series("matrix", result)
    values = [s.value for s in series.samples]
    assert math.isnan(values[0]) and values[1:] == [math.inf, -math.inf]


@pytest.mark.parametrize(
    "value, match",
    [
        ("not base64!", "not valid"),
        ("abc", "not valid base64"),
        ("W3s!fV0=", "not valid base64"),  # a character outside the alphabet
        (base64.b64encode(b"not json").decode(), "not valid JSON"),
        (b64({"metric": {}}), "not a JSON array"),
        (b"{not json", "not valid JSON"),
        (123, "expected base64 str or bytes"),
    ],
)
def test_malformed_payload_raises(value, match):
    with pytest.raises(MalformedResultError, match=match):
        decode_result({"resultType": "vector", "resultJson": value})


@pytest.mark.parametrize(
    "result",
    [
        ["not an object"],
        [{"metric": {}, "value": [1]}],
        [{"metric": {}, "value": ["t", "1"]}],
        [{"metric": {}, "values": [[1, "nope"]]}],
    ],
)
def test_malformed_entries_raise(result):
    with pytest.raises(MalformedResultError):
        to_series("vector", result)


def test_histogram_points_stay_in_raw():
    entry = {"metric": {"le": "x"}, "histogram": [1, {"count": "2"}]}
    (series,) = to_series("vector", [entry])
    assert series.samples == ()
    assert series.raw == entry


def test_unsupported_source_type():
    with pytest.raises(TypeError, match="expected a metrics query response"):
        decode_result(42)


def test_json_lines():
    lines = [b64({"_msg": "hello", "_time": "t1"}), base64.b64encode(b"plain log line").decode()]
    assert decode_json_lines(lines) == [{"_msg": "hello", "_time": "t1"}, "plain log line"]
    assert decode_json_lines(None) == []
    assert decode_json_lines([]) == []
