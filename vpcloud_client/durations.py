# coding: utf-8

"""
    Durations for the Observatory APIs.

    The APIs take a duration, such as a range query's or a Watch's `step`, as a
    protobuf Duration, whose JSON form is seconds: "300s" or "1.5s". The SDK
    also accepts what people write in PromQL ("5m", "1h30m", "500ms"), seconds
    as a number or a numeric string, and a datetime.timedelta.

    to_duration_seconds converts any of them for a request, which needs a
    positive duration. normalize_duration is the lenient form the generated
    models use: it also accepts zero and negative durations, and returns a
    string already in seconds unchanged, so a Duration the API sends back
    parses as sent.

        from vpcloud_client.durations import to_duration_seconds

        to_duration_seconds("5m")                           # "300s"
        to_duration_seconds(datetime.timedelta(minutes=5))  # "300s"
        to_duration_seconds(0.5)                            # "0.5s"
"""  # noqa: E501

import datetime
import numbers
import re
from decimal import Decimal
from typing import Optional, Tuple, Union

__all__ = ("Duration", "normalize_duration", "to_duration_seconds")

Duration = Union[str, int, float, Decimal, numbers.Real, datetime.timedelta]

# A protobuf Duration holds up to 10,000 years either way, in nanoseconds.
_MAX_SECONDS = Decimal(315_576_000_000)
_NANOSECOND = Decimal("1e-9")

_PROTOBUF = re.compile(r"(-?\d+(?:\.\d{1,9})?)s")
# Plain seconds, as Prometheus' query_range takes `step`.
_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
# Prometheus' duration grammar: whole numbers, each unit at most once, largest first.
_PROMETHEUS = re.compile(r"(?:(\d+)y)?(?:(\d+)w)?(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?(?:(\d+)ms)?")
_PROMETHEUS_UNIT_MS = (365 * 86_400_000, 7 * 86_400_000, 86_400_000, 3_600_000, 60_000, 1_000, 1)

_ACCEPTED = (
    'a number of seconds (300, 1.5, "300"), a datetime.timedelta, "300s", "1.5s", or a Prometheus '
    'duration such as "5m", "1h30m" or "500ms" (units y, w, d, h, m, s, ms)'
)


def to_duration_seconds(value: Duration) -> str:
    """Convert a duration to the seconds form the Observatory APIs take, for a
    request: the duration must be positive.

    Args:
        value: seconds as a number (int, float, Decimal, Fraction, or any
            numbers.Real such as numpy's) or a numeric string ("300", "1.5");
            a datetime.timedelta; a string already in seconds ("300s",
            "1.5s"); or a Prometheus duration ("5m", "1h30m", "1d", "500ms",
            where y is 365d and w is 7d).

    Returns:
        The duration in seconds with no trailing zeros: "300s", "0.5s".

    Raises:
        ValueError: the value is not one of those forms, is not positive, or
            is longer than a protobuf Duration holds (10,000 years).
    """
    seconds, _ = _parse(value)
    if seconds <= 0:
        raise ValueError(f"duration must be positive, got {value!r}; use {_ACCEPTED}")
    return _format(seconds)


def normalize_duration(value: Duration) -> str:
    """Convert a duration to seconds as to_duration_seconds does, but accept
    anything a protobuf Duration holds, zero and negative included. A string
    already in seconds ("0s", "1.500s", "-2s") is returned unchanged.

    Raises:
        ValueError: the value is not an accepted form, or is beyond 10,000
            years either way.
    """
    seconds, protobuf = _parse(value)
    return protobuf if protobuf is not None else _format(seconds)


def _format(seconds: Decimal) -> str:
    text = f"{seconds.normalize():f}"
    return f"{'0' if text in ('0', '-0') else text}s"


def _parse(value: Duration) -> Tuple[Decimal, Optional[str]]:
    """The duration in seconds, rounded to nanoseconds, and the value itself
    when it was already a protobuf seconds string."""
    protobuf = None
    if isinstance(value, str) and _PROTOBUF.fullmatch(value.strip()):
        protobuf = value.strip()
    seconds = _seconds(value)
    if abs(seconds) > _MAX_SECONDS:
        raise ValueError(f"duration {value!r} is beyond the 10,000 years the API accepts")
    rounded = seconds.quantize(_NANOSECOND)
    if rounded == 0 and seconds != 0:
        raise ValueError(f"duration {value!r} is shorter than a nanosecond; use {_ACCEPTED}")
    return rounded, protobuf


def _seconds(value: Duration) -> Decimal:
    if isinstance(value, datetime.timedelta):
        microseconds = (value.days * 86_400 + value.seconds) * 1_000_000 + value.microseconds
        return Decimal(microseconds).scaleb(-6)
    if isinstance(value, bool):
        raise ValueError(f"invalid duration {value!r}; use {_ACCEPTED}")
    if isinstance(value, Decimal):
        return _finite(value, value)
    if isinstance(value, numbers.Integral):
        return Decimal(int(value))
    if isinstance(value, numbers.Rational):
        return Decimal(int(value.numerator)) / Decimal(int(value.denominator))
    if isinstance(value, numbers.Real):
        return _finite(Decimal(repr(float(value))), value)
    if isinstance(value, str):
        text = value.strip()
        match = _PROTOBUF.fullmatch(text)
        if match:
            return Decimal(match.group(1))
        if _NUMBER.fullmatch(text):
            return Decimal(text)
        match = _PROMETHEUS.fullmatch(text)
        if text and match:
            milliseconds = sum(int(n) * unit for n, unit in zip(match.groups(), _PROMETHEUS_UNIT_MS) if n)
            return Decimal(milliseconds).scaleb(-3)
    raise ValueError(f"invalid duration {value!r}; use {_ACCEPTED}")


def _finite(seconds: Decimal, value: object) -> Decimal:
    if not seconds.is_finite():
        raise ValueError(f"invalid duration {value!r}; use {_ACCEPTED}")
    return seconds
