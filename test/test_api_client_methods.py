# coding: utf-8

"""
    Tests for vpcloud_client.api_client module — serialization, deserialization,
    and helper methods.
"""

import datetime
import decimal
import json
import os
import tempfile
import uuid
import pytest
from enum import Enum
from unittest.mock import Mock, patch, MagicMock

from pydantic import SecretStr

from vpcloud_client.api_client import ApiClient
from vpcloud_client.configuration import Configuration
from vpcloud_client.exceptions import ApiException, ApiValueError
from test.utils import MockResponse


class TestApiClientLifecycle:
    """Tests for ApiClient context manager and defaults."""

    def test_context_manager(self):
        config = Configuration(host="https://test.example.com")
        with ApiClient(config) as client:
            assert client is not None

    def test_set_default_header(self):
        config = Configuration(host="https://test.example.com")
        client = ApiClient(config)
        client.set_default_header("X-Custom", "value")
        assert client.default_headers["X-Custom"] == "value"

    def test_user_agent(self):
        config = Configuration(host="https://test.example.com")
        client = ApiClient(config)
        client.user_agent = "my-agent/1.0"
        assert client.user_agent == "my-agent/1.0"

    def test_cookie(self):
        config = Configuration(host="https://test.example.com")
        client = ApiClient(config, cookie="session=abc")
        assert client.cookie == "session=abc"

    def test_header_name_value(self):
        config = Configuration(host="https://test.example.com")
        client = ApiClient(config, header_name="X-Api-Key", header_value="key123")
        assert client.default_headers["X-Api-Key"] == "key123"


class TestSanitizeForSerialization:
    """Tests for sanitize_for_serialization method."""

    def _client(self):
        return ApiClient(Configuration(host="https://test.example.com"))

    def test_none(self):
        assert self._client().sanitize_for_serialization(None) is None

    def test_primitive_str(self):
        assert self._client().sanitize_for_serialization("hello") == "hello"

    def test_primitive_int(self):
        assert self._client().sanitize_for_serialization(42) == 42

    def test_primitive_float(self):
        assert self._client().sanitize_for_serialization(3.14) == 3.14

    def test_primitive_bool(self):
        assert self._client().sanitize_for_serialization(True) is True

    def test_enum(self):
        class Color(Enum):
            RED = "red"
        assert self._client().sanitize_for_serialization(Color.RED) == "red"

    def test_secret_str(self):
        secret = SecretStr("my-secret")
        assert self._client().sanitize_for_serialization(secret) == "my-secret"

    def test_uuid(self):
        u = uuid.UUID("12345678-1234-5678-1234-567812345678")
        assert self._client().sanitize_for_serialization(u) == str(u)

    def test_list(self):
        result = self._client().sanitize_for_serialization([1, "two", 3.0])
        assert result == [1, "two", 3.0]

    def test_tuple(self):
        result = self._client().sanitize_for_serialization((1, "two"))
        assert result == (1, "two")

    def test_datetime(self):
        dt = datetime.datetime(2024, 1, 15, 12, 30, 0)
        result = self._client().sanitize_for_serialization(dt)
        assert result == dt.isoformat()

    def test_date(self):
        d = datetime.date(2024, 1, 15)
        result = self._client().sanitize_for_serialization(d)
        assert result == "2024-01-15"

    def test_decimal(self):
        d = decimal.Decimal("3.14159")
        result = self._client().sanitize_for_serialization(d)
        assert result == "3.14159"

    def test_dict(self):
        result = self._client().sanitize_for_serialization({"key": "value", "num": 1})
        assert result == {"key": "value", "num": 1}

    def test_nested_dict(self):
        result = self._client().sanitize_for_serialization({"a": {"b": [1, 2]}})
        assert result == {"a": {"b": [1, 2]}}

    def test_object_with_to_dict(self):
        obj = Mock()
        obj.to_dict.return_value = {"field": "value"}
        result = self._client().sanitize_for_serialization(obj)
        assert result == {"field": "value"}

    def test_object_with_dict(self):
        class Simple:
            def __init__(self):
                self.x = 1
                self.y = "two"
        result = self._client().sanitize_for_serialization(Simple())
        assert result == {"x": 1, "y": "two"}

    def test_bytes(self):
        result = self._client().sanitize_for_serialization(b"data")
        assert result == b"data"


class TestDeserialize:
    """Tests for deserialize method."""

    def _client(self):
        return ApiClient(Configuration(host="https://test.example.com"))

    def test_json_content_type(self):
        result = self._client().deserialize('{"key":"val"}', 'object', 'application/json')
        assert result == {"key": "val"}

    def test_json_empty_string(self):
        result = self._client().deserialize('', 'object', 'application/json')
        assert result == ""

    def test_text_content_type(self):
        result = self._client().deserialize('hello world', 'str', 'text/plain')
        assert result == "hello world"

    def test_none_content_type(self):
        result = self._client().deserialize('{"a":1}', 'object', None)
        assert result == {"a": 1}

    def test_none_content_type_non_json(self):
        result = self._client().deserialize('just text', 'str', None)
        assert result == "just text"

    def test_unsupported_content_type(self):
        with pytest.raises(ApiException):
            self._client().deserialize('data', 'str', 'application/octet-stream')

    def test_json_subtype(self):
        result = self._client().deserialize('{"a":1}', 'object', 'application/vnd.api+json')
        assert result == {"a": 1}

    def test_deserialize_int(self):
        result = self._client().deserialize('42', 'int', 'application/json')
        assert result == 42

    def test_deserialize_float(self):
        result = self._client().deserialize('3.14', 'float', 'application/json')
        assert result == 3.14

    def test_deserialize_bool(self):
        result = self._client().deserialize('true', 'bool', 'application/json')
        assert result is True

    def test_deserialize_str(self):
        result = self._client().deserialize('"hello"', 'str', 'application/json')
        assert result == "hello"

    def test_deserialize_date(self):
        result = self._client().deserialize('"2024-01-15"', 'date', 'application/json')
        assert result == datetime.date(2024, 1, 15)

    def test_deserialize_datetime(self):
        result = self._client().deserialize('"2024-01-15T12:30:00"', 'datetime', 'application/json')
        assert isinstance(result, datetime.datetime)

    def test_deserialize_decimal(self):
        result = self._client().deserialize('"3.14"', 'decimal', 'application/json')
        assert result == decimal.Decimal("3.14")

    def test_deserialize_list(self):
        result = self._client().deserialize('[1,2,3]', 'List[int]', 'application/json')
        assert result == [1, 2, 3]

    def test_deserialize_dict(self):
        result = self._client().deserialize('{"a":"b"}', 'Dict[str, str]', 'application/json')
        assert result == {"a": "b"}


class TestSelectHeaders:
    """Tests for header selection methods."""

    def _client(self):
        return ApiClient(Configuration(host="https://test.example.com"))

    def test_select_accept_json(self):
        result = self._client().select_header_accept(["application/json", "text/plain"])
        assert result == "application/json"

    def test_select_accept_none(self):
        result = self._client().select_header_accept([])
        assert result is None

    def test_select_accept_fallback(self):
        result = self._client().select_header_accept(["text/plain", "text/html"])
        assert result == "text/plain"

    def test_select_content_type_json(self):
        result = self._client().select_header_content_type(["application/json", "text/plain"])
        assert result == "application/json"

    def test_select_content_type_none(self):
        result = self._client().select_header_content_type([])
        assert result is None

    def test_select_content_type_fallback(self):
        result = self._client().select_header_content_type(["text/plain"])
        assert result == "text/plain"


class TestParametersToTuples:
    """Tests for parameters_to_tuples method."""

    def _client(self):
        return ApiClient(Configuration(host="https://test.example.com"))

    def test_dict_params(self):
        result = self._client().parameters_to_tuples({"a": "1", "b": "2"}, None)
        assert ("a", "1") in result
        assert ("b", "2") in result

    def test_multi_collection(self):
        result = self._client().parameters_to_tuples(
            {"tags": ["a", "b"]}, {"tags": "multi"}
        )
        assert ("tags", "a") in result
        assert ("tags", "b") in result

    def test_csv_collection(self):
        result = self._client().parameters_to_tuples(
            {"tags": ["a", "b"]}, {"tags": "csv"}
        )
        assert ("tags", "a,b") in result

    def test_ssv_collection(self):
        result = self._client().parameters_to_tuples(
            {"tags": ["a", "b"]}, {"tags": "ssv"}
        )
        assert ("tags", "a b") in result

    def test_tsv_collection(self):
        result = self._client().parameters_to_tuples(
            {"tags": ["a", "b"]}, {"tags": "tsv"}
        )
        assert ("tags", "a\tb") in result

    def test_pipes_collection(self):
        result = self._client().parameters_to_tuples(
            {"tags": ["a", "b"]}, {"tags": "pipes"}
        )
        assert ("tags", "a|b") in result


class TestParametersToUrlQuery:
    """Tests for parameters_to_url_query method."""

    def _client(self):
        return ApiClient(Configuration(host="https://test.example.com"))

    def test_simple_params(self):
        result = self._client().parameters_to_url_query({"key": "val"}, None)
        assert "key=val" in result

    def test_bool_param(self):
        result = self._client().parameters_to_url_query({"active": True}, None)
        assert "active=true" in result

    def test_int_param(self):
        result = self._client().parameters_to_url_query({"count": 10}, None)
        assert "count=10" in result

    def test_dict_param(self):
        result = self._client().parameters_to_url_query({"filter": {"a": 1}}, None)
        assert "filter=" in result

    def test_multi_collection(self):
        result = self._client().parameters_to_url_query(
            {"tags": ["a", "b"]}, {"tags": "multi"}
        )
        assert "tags=a" in result
        assert "tags=b" in result

    def test_csv_collection(self):
        result = self._client().parameters_to_url_query(
            {"tags": ["a", "b"]}, {"tags": "csv"}
        )
        assert "tags=a%2Cb" in result or "tags=a,b" in result


class TestUpdateParamsForAuth:
    """Tests for update_params_for_auth method."""

    def _client(self):
        return ApiClient(Configuration(host="https://test.example.com"))

    def test_no_auth_settings(self):
        client = self._client()
        headers = {}
        queries = []
        client.update_params_for_auth(headers, queries, [], "/", "GET", None)
        assert "Authorization" not in headers

    def test_bearer_auth(self):
        config = Configuration(host="https://test.example.com", access_token="test-token")
        client = ApiClient(config)
        headers = {}
        queries = []
        client.update_params_for_auth(headers, queries, ["bearerAuth"], "/", "GET", None)
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test-token"

    def test_cookie_auth(self):
        client = self._client()
        headers = {}
        queries = []
        auth_setting = {"type": "api_key", "in": "cookie", "key": "session", "value": "abc123"}
        client._apply_auth_params(headers, queries, "/", "GET", None, auth_setting)
        assert headers["Cookie"] == "abc123"

    def test_query_auth(self):
        client = self._client()
        headers = {}
        queries = []
        auth_setting = {"type": "api_key", "in": "query", "key": "api_key", "value": "mykey"}
        client._apply_auth_params(headers, queries, "/", "GET", None, auth_setting)
        assert ("api_key", "mykey") in queries

    def test_invalid_auth_location(self):
        client = self._client()
        with pytest.raises(ApiValueError):
            client._apply_auth_params({}, [], "/", "GET", None, {"type": "api_key", "in": "body", "key": "k", "value": "v"})

    def test_request_auth_override(self):
        client = self._client()
        headers = {}
        queries = []
        request_auth = {"type": "bearer", "in": "header", "key": "Authorization", "value": "Bearer override"}
        client.update_params_for_auth(headers, queries, ["bearerAuth"], "/", "GET", None, request_auth=request_auth)
        assert headers["Authorization"] == "Bearer override"


class TestFilesParameters:
    """Tests for files_parameters method."""

    def _client(self):
        return ApiClient(Configuration(host="https://test.example.com"))

    def test_bytes_file(self):
        params = self._client().files_parameters({"file": b"content"})
        assert len(params) == 1
        assert params[0][0] == "file"

    def test_tuple_file(self):
        params = self._client().files_parameters({"file": ("name.txt", b"content")})
        assert len(params) == 1

    def test_list_of_bytes(self):
        params = self._client().files_parameters({"files": [b"one", b"two"]})
        assert len(params) == 2

    def test_unsupported_file_value(self):
        with pytest.raises(ValueError):
            self._client().files_parameters({"file": 12345})


class TestResponseDeserialize:
    """Tests for response_deserialize method."""

    def _client(self):
        return ApiClient(Configuration(host="https://test.example.com"))

    def test_success_json(self):
        resp = MockResponse(200, headers={"content-type": "application/json"}, data=b'{"name":"test"}')
        result = self._client().response_deserialize(resp, {"200": "object"})
        assert result.status_code == 200
        assert result.data == {"name": "test"}

    def test_no_matching_type(self):
        resp = MockResponse(200, headers={"content-type": "application/json"}, data=b'{"name":"test"}')
        result = self._client().response_deserialize(resp, {"201": "object"})
        assert result.status_code == 200

    def test_2xx_wildcard(self):
        resp = MockResponse(201, headers={"content-type": "application/json"}, data=b'{"id":"1"}')
        result = self._client().response_deserialize(resp, {"2XX": "object"})
        assert result.status_code == 201
        assert result.data == {"id": "1"}

    def test_error_response(self):
        resp = MockResponse(400, headers={"content-type": "application/json"}, data=b'{"error":"bad"}')
        with pytest.raises(ApiException):
            self._client().response_deserialize(resp, {"400": "object"})

    def test_bytearray_response(self):
        resp = MockResponse(200, headers={"content-type": "application/octet-stream"}, data=b'\x00\x01\x02')
        result = self._client().response_deserialize(resp, {"200": "bytearray"})
        assert result.data == b'\x00\x01\x02'

    def test_charset_encoding(self):
        resp = MockResponse(200, headers={"content-type": "application/json; charset=utf-8"}, data=b'{"a":1}')
        result = self._client().response_deserialize(resp, {"200": "object"})
        assert result.data == {"a": 1}


class TestCallApi:
    """Tests for call_api without retry."""

    def _client(self):
        config = Configuration(host="https://test.example.com")
        return ApiClient(config)

    def test_direct_call(self):
        client = self._client()
        mock_resp = MockResponse(200, data=b'{}')
        with patch.object(client.rest_client, 'request', return_value=mock_resp):
            result = client.call_api("GET", "https://test.example.com/api")
            assert result.status == 200

    def test_direct_call_api_exception(self):
        client = self._client()
        with patch.object(client.rest_client, 'request', side_effect=ApiException(status=500, reason="Error")):
            with pytest.raises(ApiException):
                client.call_api("GET", "https://test.example.com/api")
