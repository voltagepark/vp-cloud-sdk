# coding: utf-8

"""
    Idempotency key generation unit tests for vpcloud_client.

    The tests find their operations in the generated APIs rather than naming
    them, so they keep working as operations are added to or removed from the
    spec.
"""  # noqa: E501

import importlib
import inspect
import pkgutil
import uuid

import pytest

import vpcloud_client.api
from vpcloud_client import ApiClient, Configuration


def _serializers():
    """Yields (api class, serializer name, HTTP method) for every generated operation."""
    for module_info in pkgutil.iter_modules(vpcloud_client.api.__path__):
        module = importlib.import_module(f"vpcloud_client.api.{module_info.name}")
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if not cls.__name__.endswith("Api") or cls.__module__ != module.__name__:
                continue
            for name, fn in inspect.getmembers(cls, inspect.isfunction):
                if not (name.startswith("_") and name.endswith("_serialize")):
                    continue
                source = inspect.getsource(fn)
                for method in ("POST", "PUT", "PATCH", "DELETE", "GET"):
                    if f"method='{method}'" in source:
                        yield cls, name, method
                        break


def _find(method, with_param=None):
    for cls, name, m in _serializers():
        if m != method:
            continue
        if with_param and with_param not in inspect.signature(getattr(cls, name)).parameters:
            continue
        return cls, name
    pytest.skip(f"no generated {method} operation{' with ' + with_param if with_param else ''}")


def _config(**kwargs):
    # Observatory operations fail closed without an Observatory token, even
    # when only serialized; give them one so every operation can be built.
    return Configuration(observatory_access_token="test-token", **kwargs)


def _headers(config, cls, name, **overrides):
    api = cls(api_client=ApiClient(config))
    fn = getattr(api, name)
    kwargs = {p: None for p in inspect.signature(fn).parameters}
    kwargs["_host_index"] = 0
    kwargs.update(overrides)
    # RequestSerialized is a tuple: (method, url, header_params, body, files)
    return fn(**kwargs)[2]


class TestIdempotencyKeys:
    """Idempotency key generation tests"""

    def test_auto_generate_idempotency_key_post(self):
        cls, name = _find("POST")
        headers = _headers(_config(auto_idempotency_key=True), cls, name)
        uuid.UUID(headers["Idempotency-Key"])

    def test_no_idempotency_key_get(self):
        cls, name = _find("GET")
        headers = _headers(_config(auto_idempotency_key=True), cls, name)
        assert "Idempotency-Key" not in headers

    def test_auto_idempotency_key_disabled(self):
        cls, name = _find("POST")
        headers = _headers(_config(auto_idempotency_key=False), cls, name)
        assert "Idempotency-Key" not in headers

    def test_preserves_existing_idempotency_key(self):
        cls, name = _find("POST", with_param="idempotency_key")
        headers = _headers(_config(auto_idempotency_key=True), cls, name, idempotency_key="custom-key-12345")
        assert headers["Idempotency-Key"] == "custom-key-12345"

    def test_custom_idempotency_key_generator(self):
        cls, name = _find("POST")
        config = _config(auto_idempotency_key=True, idempotency_key_generator=lambda: "custom-generated-key")
        headers = _headers(config, cls, name)
        assert headers["Idempotency-Key"] == "custom-generated-key"

    def test_every_mutation_gets_a_key(self):
        config = _config(auto_idempotency_key=True)
        mutations = [(cls, name) for cls, name, m in _serializers() if m != "GET"]
        assert mutations, "no generated mutation operations"
        for cls, name in mutations:
            assert "Idempotency-Key" in _headers(config, cls, name), f"{cls.__name__}.{name}"
