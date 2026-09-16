# coding: utf-8

"""
    Tests for vpcloud_client.rest module.
"""

import json
import ssl
import pytest
from unittest.mock import Mock, patch, MagicMock

from vpcloud_client.rest import RESTResponse, RESTClientObject, is_socks_proxy_url
from vpcloud_client.exceptions import ApiException, ApiValueError
from vpcloud_client import Configuration


class TestIsSocksProxyUrl:
    """Tests for is_socks_proxy_url helper."""

    def test_none_url(self):
        assert is_socks_proxy_url(None) is False

    def test_no_scheme(self):
        assert is_socks_proxy_url("example.com") is False

    def test_http_url(self):
        assert is_socks_proxy_url("http://proxy.example.com") is False

    def test_https_url(self):
        assert is_socks_proxy_url("https://proxy.example.com") is False

    def test_socks5_url(self):
        assert is_socks_proxy_url("socks5://proxy.example.com") is True

    def test_socks5h_url(self):
        assert is_socks_proxy_url("socks5h://proxy.example.com") is True

    def test_socks4_url(self):
        assert is_socks_proxy_url("socks4://proxy.example.com") is True

    def test_socks4a_url(self):
        assert is_socks_proxy_url("socks4a://proxy.example.com") is True

    def test_socks5_uppercase(self):
        assert is_socks_proxy_url("SOCKS5://proxy.example.com") is True


class TestRESTResponse:
    """Tests for RESTResponse class."""

    def _make_response(self, status=200, reason="OK", data=b"hello"):
        resp = Mock()
        resp.status = status
        resp.reason = reason
        resp.data = data
        resp.headers = {"Content-Type": "application/json", "X-Custom": "value"}
        return resp

    def test_init(self):
        resp = self._make_response()
        rest_resp = RESTResponse(resp)
        assert rest_resp.status == 200
        assert rest_resp.reason == "OK"
        assert rest_resp.data is None

    def test_read(self):
        resp = self._make_response(data=b'{"key":"value"}')
        rest_resp = RESTResponse(resp)
        result = rest_resp.read()
        assert result == b'{"key":"value"}'

    def test_read_cached(self):
        resp = self._make_response(data=b"data")
        rest_resp = RESTResponse(resp)
        first = rest_resp.read()
        second = rest_resp.read()
        assert first == second

    def test_getheaders(self):
        resp = self._make_response()
        rest_resp = RESTResponse(resp)
        headers = rest_resp.getheaders()
        assert headers["Content-Type"] == "application/json"

    def test_getheader_exists(self):
        resp = self._make_response()
        rest_resp = RESTResponse(resp)
        assert rest_resp.getheader("X-Custom") == "value"

    def test_getheader_missing_with_default(self):
        resp = self._make_response()
        rest_resp = RESTResponse(resp)
        assert rest_resp.getheader("X-Missing", "fallback") == "fallback"

    def test_getheader_missing_no_default(self):
        resp = self._make_response()
        rest_resp = RESTResponse(resp)
        assert rest_resp.getheader("X-Missing") is None


class TestRESTClientObject:
    """Tests for RESTClientObject."""

    def _make_config(self, **kwargs):
        config = Configuration(host="https://api.test.example.com")
        config.verify_ssl = kwargs.get("verify_ssl", True)
        config.ssl_ca_cert = kwargs.get("ssl_ca_cert", None)
        config.cert_file = kwargs.get("cert_file", None)
        config.key_file = kwargs.get("key_file", None)
        config.ca_cert_data = kwargs.get("ca_cert_data", None)
        config.assert_hostname = kwargs.get("assert_hostname", None)
        config.retries = kwargs.get("retries", None)
        config.tls_server_name = kwargs.get("tls_server_name", None)
        config.socket_options = kwargs.get("socket_options", None)
        config.connection_pool_maxsize = kwargs.get("connection_pool_maxsize", None)
        config.proxy = kwargs.get("proxy", None)
        config.proxy_headers = kwargs.get("proxy_headers", None)
        return config

    def test_init_default(self):
        config = self._make_config()
        client = RESTClientObject(config)
        assert client.pool_manager is not None

    def test_init_verify_ssl_false(self):
        config = self._make_config(verify_ssl=False)
        client = RESTClientObject(config)
        assert client.pool_manager is not None

    def test_init_with_assert_hostname(self):
        config = self._make_config(assert_hostname="example.com")
        client = RESTClientObject(config)
        assert client.pool_manager is not None

    def test_init_with_retries(self):
        config = self._make_config(retries=3)
        client = RESTClientObject(config)
        assert client.pool_manager is not None

    def test_init_with_tls_server_name(self):
        config = self._make_config(tls_server_name="example.com")
        client = RESTClientObject(config)
        assert client.pool_manager is not None

    def test_init_with_socket_options(self):
        import socket
        config = self._make_config(socket_options=[(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)])
        client = RESTClientObject(config)
        assert client.pool_manager is not None

    def test_init_with_connection_pool_maxsize(self):
        config = self._make_config(connection_pool_maxsize=10)
        client = RESTClientObject(config)
        assert client.pool_manager is not None

    def test_init_with_http_proxy(self):
        config = self._make_config(proxy="http://proxy.example.com:8080", proxy_headers={"Proxy-Auth": "token"})
        client = RESTClientObject(config)
        assert client.pool_manager is not None

    def test_request_get(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b'{"ok": true}'
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request("GET", "https://example.com/api")
            assert response.status == 200

    def test_request_post_json(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 201
        mock_resp.reason = "Created"
        mock_resp.data = b'{}'
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "POST", "https://example.com/api",
                headers={"Content-Type": "application/json"},
                body={"key": "value"}
            )
            assert response.status == 201

    def test_request_post_no_content_type(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b'{}'
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "POST", "https://example.com/api",
                body={"key": "value"}
            )
            assert response.status == 200

    def test_request_post_form_urlencoded(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b''
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "POST", "https://example.com/api",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                post_params=[("field", "value")]
            )
            assert response.status == 200

    def test_request_post_multipart(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b''
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "POST", "https://example.com/api",
                headers={"Content-Type": "multipart/form-data"},
                post_params=[("file", b"content")]
            )
            assert response.status == 200

    def test_request_post_string_body(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b''
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "POST", "https://example.com/api",
                headers={"Content-Type": "text/plain"},
                body="raw text"
            )
            assert response.status == 200

    def test_request_post_text_bool_body(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b''
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "POST", "https://example.com/api",
                headers={"Content-Type": "text/plain"},
                body=True
            )
            assert response.status == 200

    def test_request_post_unsupported_content_type(self):
        config = self._make_config()
        client = RESTClientObject(config)
        with pytest.raises(ApiException):
            client.request(
                "POST", "https://example.com/api",
                headers={"Content-Type": "application/octet-stream"},
                body=12345
            )

    def test_request_body_and_post_params_raises(self):
        config = self._make_config()
        client = RESTClientObject(config)
        with pytest.raises(ApiValueError):
            client.request(
                "POST", "https://example.com/api",
                body={"key": "value"},
                post_params=[("field", "value")]
            )

    def test_request_with_timeout_int(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b'{}'
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "GET", "https://example.com/api",
                _request_timeout=30
            )
            assert response.status == 200

    def test_request_with_timeout_tuple(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b'{}'
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "GET", "https://example.com/api",
                _request_timeout=(5, 30)
            )
            assert response.status == 200

    def test_request_ssl_error(self):
        import urllib3
        config = self._make_config()
        client = RESTClientObject(config)
        with patch.object(client.pool_manager, 'request', side_effect=urllib3.exceptions.SSLError("SSL failed")):
            with pytest.raises(ApiException) as exc_info:
                client.request("GET", "https://example.com/api")
            assert "SSLError" in str(exc_info.value)

    def test_request_delete(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 204
        mock_resp.reason = "No Content"
        mock_resp.data = b''
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request("DELETE", "https://example.com/api/1")
            assert response.status == 204

    def test_request_put(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b'{}'
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "PUT", "https://example.com/api/1",
                headers={"Content-Type": "application/json"},
                body={"updated": True}
            )
            assert response.status == 200

    def test_request_patch(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b'{}'
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "PATCH", "https://example.com/api/1",
                body=None
            )
            assert response.status == 200

    def test_request_head(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b''
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request("HEAD", "https://example.com/api")
            assert response.status == 200

    def test_request_multipart_with_dict_value(self):
        config = self._make_config()
        client = RESTClientObject(config)
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.reason = "OK"
        mock_resp.data = b''
        mock_resp.headers = {}
        with patch.object(client.pool_manager, 'request', return_value=mock_resp):
            response = client.request(
                "POST", "https://example.com/api",
                headers={"Content-Type": "multipart/form-data"},
                post_params=[("metadata", {"key": "value"})]
            )
            assert response.status == 200
