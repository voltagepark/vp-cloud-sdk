# coding: utf-8

"""
    Tests for vpcloud_client.exceptions module.
"""

import pytest
from unittest.mock import Mock

from vpcloud_client.exceptions import (
    OpenApiException,
    ApiTypeError,
    ApiValueError,
    ApiAttributeError,
    ApiKeyError,
    ApiException,
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    ServiceException,
    ConflictException,
    UnprocessableEntityException,
    render_path,
)


class TestRenderPath:
    """Tests for render_path helper."""

    def test_empty_path(self):
        assert render_path([]) == ""

    def test_string_keys(self):
        assert render_path(["a", "b"]) == "['a']['b']"

    def test_integer_keys(self):
        assert render_path([0, 1]) == "[0][1]"

    def test_mixed_keys(self):
        assert render_path(["items", 0, "name"]) == "['items'][0]['name']"


class TestApiTypeError:
    """Tests for ApiTypeError."""

    def test_basic(self):
        err = ApiTypeError("bad type")
        assert str(err) == "bad type"

    def test_with_path(self):
        err = ApiTypeError("bad type", path_to_item=["a", 0])
        assert "['a'][0]" in str(err)
        assert err.path_to_item == ["a", 0]

    def test_with_valid_classes(self):
        err = ApiTypeError("bad type", valid_classes=(str, int))
        assert err.valid_classes == (str, int)

    def test_with_key_type(self):
        err = ApiTypeError("bad type", key_type=True)
        assert err.key_type is True


class TestApiValueError:
    """Tests for ApiValueError."""

    def test_basic(self):
        err = ApiValueError("bad value")
        assert str(err) == "bad value"

    def test_with_path(self):
        err = ApiValueError("bad value", path_to_item=["field"])
        assert "['field']" in str(err)
        assert err.path_to_item == ["field"]


class TestApiAttributeError:
    """Tests for ApiAttributeError."""

    def test_basic(self):
        err = ApiAttributeError("missing attr")
        assert str(err) == "missing attr"

    def test_with_path(self):
        err = ApiAttributeError("missing attr", path_to_item=["obj", "field"])
        assert "['obj']['field']" in str(err)


class TestApiKeyError:
    """Tests for ApiKeyError."""

    def test_basic(self):
        err = ApiKeyError("missing key")
        assert err.path_to_item is None

    def test_with_path(self):
        err = ApiKeyError("missing key", path_to_item=["dict", "key"])
        assert err.path_to_item == ["dict", "key"]


class TestApiException:
    """Tests for ApiException."""

    def test_basic(self):
        err = ApiException(status=500, reason="Internal Server Error")
        assert err.status == 500
        assert err.reason == "Internal Server Error"
        assert err.body is None
        assert err.headers is None

    def test_with_body_and_data(self):
        err = ApiException(status=400, reason="Bad Request", body="error body", data={"error": "details"})
        assert err.body == "error body"
        assert err.data == {"error": "details"}

    def test_with_http_resp(self):
        mock_resp = Mock()
        mock_resp.status = 404
        mock_resp.reason = "Not Found"
        mock_resp.data = b"not found"
        mock_resp.getheaders.return_value = {"Content-Type": "text/plain"}
        err = ApiException(http_resp=mock_resp)
        assert err.status == 404
        assert err.reason == "Not Found"
        assert err.body == "not found"
        assert err.headers == {"Content-Type": "text/plain"}

    def test_with_http_resp_decode_error(self):
        mock_resp = Mock()
        mock_resp.status = 500
        mock_resp.reason = "Error"
        mock_resp.data = Mock()
        mock_resp.data.decode.side_effect = Exception("decode failed")
        mock_resp.getheaders.return_value = {}
        err = ApiException(http_resp=mock_resp)
        assert err.status == 500
        assert err.body is None

    def test_str_with_headers(self):
        mock_resp = Mock()
        mock_resp.status = 401
        mock_resp.reason = "Unauthorized"
        mock_resp.data = b"denied"
        mock_resp.getheaders.return_value = {"WWW-Authenticate": "Bearer"}
        err = ApiException(http_resp=mock_resp)
        s = str(err)
        assert "(401)" in s
        assert "Unauthorized" in s
        assert "WWW-Authenticate" in s
        assert "denied" in s

    def test_str_with_data(self):
        err = ApiException(status=422, reason="Unprocessable", data={"field": "invalid"})
        s = str(err)
        assert "(422)" in s
        assert "{'field': 'invalid'}" in s

    def test_str_minimal(self):
        err = ApiException(status=200, reason="OK")
        s = str(err)
        assert "(200)" in s
        assert "OK" in s

    def test_http_resp_does_not_override_explicit_values(self):
        mock_resp = Mock()
        mock_resp.status = 500
        mock_resp.reason = "Server Error"
        mock_resp.data = b"server error"
        mock_resp.getheaders.return_value = {}
        err = ApiException(status=400, reason="Custom Reason", http_resp=mock_resp, body="custom body")
        assert err.status == 400
        assert err.reason == "Custom Reason"
        assert err.body == "custom body"


class TestApiExceptionFromResponse:
    """Tests for ApiException.from_response class method."""

    def _mock_resp(self, status):
        resp = Mock()
        resp.status = status
        resp.reason = "Error"
        resp.data = b"error"
        resp.getheaders.return_value = {}
        return resp

    def test_400_raises_bad_request(self):
        with pytest.raises(BadRequestException):
            ApiException.from_response(http_resp=self._mock_resp(400), body="err", data=None)

    def test_401_raises_unauthorized(self):
        with pytest.raises(UnauthorizedException):
            ApiException.from_response(http_resp=self._mock_resp(401), body="err", data=None)

    def test_403_raises_forbidden(self):
        with pytest.raises(ForbiddenException):
            ApiException.from_response(http_resp=self._mock_resp(403), body="err", data=None)

    def test_404_raises_not_found(self):
        with pytest.raises(NotFoundException):
            ApiException.from_response(http_resp=self._mock_resp(404), body="err", data=None)

    def test_409_raises_conflict(self):
        with pytest.raises(ConflictException):
            ApiException.from_response(http_resp=self._mock_resp(409), body="err", data=None)

    def test_422_raises_unprocessable(self):
        with pytest.raises(UnprocessableEntityException):
            ApiException.from_response(http_resp=self._mock_resp(422), body="err", data=None)

    def test_500_raises_service_exception(self):
        with pytest.raises(ServiceException):
            ApiException.from_response(http_resp=self._mock_resp(500), body="err", data=None)

    def test_502_raises_service_exception(self):
        with pytest.raises(ServiceException):
            ApiException.from_response(http_resp=self._mock_resp(502), body="err", data=None)

    def test_503_raises_service_exception(self):
        with pytest.raises(ServiceException):
            ApiException.from_response(http_resp=self._mock_resp(503), body="err", data=None)

    def test_other_status_raises_api_exception(self):
        with pytest.raises(ApiException):
            ApiException.from_response(http_resp=self._mock_resp(418), body="err", data=None)


class TestExceptionSubclasses:
    """Verify exception hierarchy."""

    def test_bad_request_is_api_exception(self):
        assert issubclass(BadRequestException, ApiException)

    def test_not_found_is_api_exception(self):
        assert issubclass(NotFoundException, ApiException)

    def test_unauthorized_is_api_exception(self):
        assert issubclass(UnauthorizedException, ApiException)

    def test_forbidden_is_api_exception(self):
        assert issubclass(ForbiddenException, ApiException)

    def test_service_is_api_exception(self):
        assert issubclass(ServiceException, ApiException)

    def test_conflict_is_api_exception(self):
        assert issubclass(ConflictException, ApiException)

    def test_unprocessable_is_api_exception(self):
        assert issubclass(UnprocessableEntityException, ApiException)

    def test_all_are_open_api_exception(self):
        for cls in [ApiTypeError, ApiValueError, ApiAttributeError, ApiKeyError, ApiException]:
            assert issubclass(cls, OpenApiException)
