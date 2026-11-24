# coding: utf-8

"""Tests for durations.to_duration_seconds and normalize_duration, and the
models whose fields take a duration (QueryRangeRequest.step). No network."""

import datetime
import decimal
import fractions
import inspect
import numbers
import re

import pydantic
import pytest

import vpcloud_client.models
from vpcloud_client.durations import normalize_duration, to_duration_seconds
from vpcloud_client.models.query_range_request import QueryRangeRequest


class FloatLike:
    """A numbers.Real that isn't a float, as numpy.float32 isn't."""

    def __init__(self, value):
        self.value = value

    def __float__(self):
        return self.value


class IntLike:
    """A numbers.Integral that isn't an int, as numpy.int64 isn't."""

    def __init__(self, value):
        self.value = value

    def __int__(self):
        return self.value


numbers.Real.register(FloatLike)
numbers.Integral.register(IntLike)


@pytest.mark.parametrize("value, expected", [
    # Already in the API's form.
    ("300s", "300s"),
    ("1.5s", "1.5s"),
    ("0.000000001s", "0.000000001s"),
    ("60.000s", "60s"),
    # Prometheus durations.
    ("5m", "300s"),
    ("1h", "3600s"),
    ("1h30m", "5400s"),
    ("1m30s", "90s"),
    ("500ms", "0.5s"),
    ("1s500ms", "1.5s"),
    ("1d", "86400s"),
    ("1w", "604800s"),
    ("1y", "31536000s"),
    ("1y2w3d4h5m6s7ms", "33019506.007s"),
    (" 5m ", "300s"),
    # Seconds as a numeric string, as Prometheus' query_range takes step.
    ("300", "300s"),
    ("1.5", "1.5s"),
    (" 15 ", "15s"),
    # Seconds as a number.
    (300, "300s"),
    (1.5, "1.5s"),
    (0.5, "0.5s"),
    (1234567, "1234567s"),
    (0.1, "0.1s"),
    (decimal.Decimal("1.50"), "1.5s"),
    (fractions.Fraction(1, 4), "0.25s"),
    (fractions.Fraction(1, 3), "0.333333333s"),
    (FloatLike(2.5), "2.5s"),
    (IntLike(60), "60s"),
    # timedelta.
    (datetime.timedelta(minutes=5), "300s"),
    (datetime.timedelta(days=1, seconds=1), "86401s"),
    (datetime.timedelta(milliseconds=250), "0.25s"),
    (datetime.timedelta(microseconds=1), "0.000001s"),
])
def test_accepted_forms(value, expected):
    assert to_duration_seconds(value) == expected
    # normalize_duration keeps a string already in seconds as written.
    kept = isinstance(value, str) and re.fullmatch(r"\d+(\.\d+)?s", value.strip())
    assert normalize_duration(value) == (value.strip() if kept else expected)


@pytest.mark.parametrize("value", [
    "", "5M", "5min", "1.5m", "1m1h", "5m5m", "s", "ms", "-5m", "1 h", "P5M", "1.0000000001s", "1e3",
    True, None, [300], float("nan"), float("inf"), decimal.Decimal("NaN"), decimal.Decimal("Infinity"),
])
def test_invalid_values_name_the_accepted_forms(value):
    for convert in (to_duration_seconds, normalize_duration):
        with pytest.raises(ValueError, match=r'"5m"') as err:
            convert(value)
        assert "invalid duration" in str(err.value)


@pytest.mark.parametrize("value", [
    0, 0.0, -1, -0.5, "0", "-60", "0s", "-1.5s", "0m", "0.0s", decimal.Decimal(0), fractions.Fraction(-1, 2),
    datetime.timedelta(0), datetime.timedelta(seconds=-5),
])
def test_requests_need_a_positive_duration(value):
    with pytest.raises(ValueError, match=r'must be positive.*"5m"'):
        to_duration_seconds(value)


@pytest.mark.parametrize("value, expected", [
    # What the API sends is kept as sent.
    ("0s", "0s"),
    ("-1.5s", "-1.5s"),
    ("1.500s", "1.500s"),
    ("-315576000000s", "-315576000000s"),
    ("0.000000001s", "0.000000001s"),
    # Other forms are converted, zero and negative included.
    (0, "0s"),
    (-0.0, "0s"),
    ("0", "0s"),
    ("-60", "-60s"),
    ("0m", "0s"),
    (datetime.timedelta(seconds=-90), "-90s"),
])
def test_normalize_duration_accepts_any_protobuf_duration(value, expected):
    assert normalize_duration(value) == expected


def test_out_of_range_is_rejected():
    for convert in (to_duration_seconds, normalize_duration):
        with pytest.raises(ValueError, match="shorter than a nanosecond"):
            convert(1e-12)
        with pytest.raises(ValueError, match="10,000 years"):
            convert("20000y")
        with pytest.raises(ValueError, match="10,000 years"):
            convert(1e300)
    with pytest.raises(ValueError, match="10,000 years"):
        normalize_duration("-315576000001s")


@pytest.mark.parametrize("step", ["5m", "300s", "300", 300, decimal.Decimal(300), datetime.timedelta(minutes=5)])
def test_query_range_request_holds_step_in_seconds(step):
    request = QueryRangeRequest(query="up", step=step)
    assert request.step == "300s"
    assert request.to_dict() == {"query": "up", "step": "300s"}


def test_query_range_request_step_assignment_and_from_dict():
    request = QueryRangeRequest(query="up")
    assert request.step is None and "step" not in request.to_dict()
    request.step = "1h"
    assert request.step == "3600s"
    assert QueryRangeRequest.from_dict({"query": "up", "step": "500ms"}).step == "0.5s"


@pytest.mark.parametrize("step", [0, -60, "0s", "-5s", datetime.timedelta(seconds=-1)])
def test_query_range_request_needs_a_positive_step(step):
    with pytest.raises(pydantic.ValidationError, match=r'must be positive.*"5m"'):
        QueryRangeRequest(query="up", step=step)


def test_query_range_request_rejects_an_invalid_step():
    with pytest.raises(pydantic.ValidationError, match=r'invalid duration .*"5m"'):
        QueryRangeRequest(query="up", step="5 minutes")


def _duration_models():
    """(model, positive) for every generated model with duration fields."""
    for _, model in inspect.getmembers(vpcloud_client.models, inspect.isclass):
        validators = model.__pydantic_decorators__.field_validators if issubclass(model, pydantic.BaseModel) else {}
        if "durations_in_seconds" in validators:
            namespace = vars(inspect.getmodule(model))
            yield model, "to_duration_seconds" in namespace, validators["durations_in_seconds"].info.fields


def test_only_request_bodies_require_positive_durations():
    """Response models must parse any Duration the API sends, "0s" included;
    only inline request bodies (QueryRangeRequest) refuse zero or negative."""
    models = list(_duration_models())
    assert {model.__name__ for model, positive, _ in models if positive} == {"QueryRangeRequest"}
    for model, positive, fields in models:
        if positive:
            continue
        for sent in ("0s", "-1.5s", "1.500s"):
            parsed = model.model_validate({field: sent for field in fields})
            assert [getattr(parsed, field) for field in fields] == [sent] * len(fields)
