# coding: utf-8

"""Routing and credential tests for the Observatory APIs (metrics, logs,
audit). Auth0 and the HTTP layer are faked; every assertion is on what the SDK
would have sent. No network."""

import base64
import json

import httpx
import pytest
import urllib3

import vpcloud_client
from vpcloud_client import credentials, rest
from vpcloud_client.credentials import AuthenticationError
from vpcloud_client.models.query_request import QueryRequest

OBS = "https://observatory.voltagepark.com"
HARBOR_SEA1 = "https://api.sea-1.voltagepark.com/harbor"
PROD = "voltagepark-harbor.us.auth0.com"
DEV = "voltagepark-dev.us.auth0.com"


class FakeResp:
    def __init__(self, status, body):
        self.status = status
        self.reason = "OK" if status == 200 else "ERR"
        self.data = json.dumps(body).encode()
        self.headers = urllib3.HTTPHeaderDict({"content-type": "application/json"})


@pytest.fixture
def wire(monkeypatch, tmp_path):
    """Fakes Auth0 and the HTTP layer; records token mints and requests."""
    monkeypatch.setenv("HOME", str(tmp_path))  # no ~/.voltagepark/credentials
    monkeypatch.setattr(credentials.CredentialProvider, "CREDENTIALS_FILE", tmp_path / ".voltagepark" / "credentials")
    for k in list(__import__("os").environ):
        if k.startswith("VPCLOUD_"):
            monkeypatch.delenv(k)

    state = {"mints": [], "requests": [], "deny": set(), "bad_secret": False, "expires_in": 86400,
             "responses": {"/v1/fleets": {"fleets": []}}}

    def fake_post(url, json=None, headers=None, timeout=None):
        domain, audience = url.split("/")[2], json["audience"]
        state["mints"].append((domain, audience))
        req = httpx.Request("POST", url)
        if state["bad_secret"]:
            return httpx.Response(401, json={"error": "access_denied", "error_description": "Unauthorized"}, request=req)
        if audience in state["deny"]:
            return httpx.Response(403, json={
                "error": "access_denied",
                "error_description": f'Client is not authorized to access "{audience}".',
            }, request=req)
        return httpx.Response(200, json={"access_token": f"tok[{domain}|{audience}]", "expires_in": state["expires_in"]}, request=req)

    def fake_request(self, method, url, headers=None, body=None, post_params=None, _request_timeout=None):
        state["requests"].append({"method": method, "url": url, "auth": (headers or {}).get("Authorization"), "body": body})
        for suffix, payload in state["responses"].items():
            if url.split("?")[0].endswith(suffix):
                return rest.RESTResponse(FakeResp(200, payload))
        return rest.RESTResponse(FakeResp(200, {}))

    monkeypatch.setattr(credentials.httpx, "post", fake_post)
    monkeypatch.setattr(rest.RESTClientObject, "request", fake_request)
    return state


def query(config, cluster="c-1"):
    with vpcloud_client.ApiClient(config) as api:
        return vpcloud_client.MetricsApi(api).query_metrics(cluster, QueryRequest(query="up"))


def test_observatory_calls_get_their_own_audience_and_host(wire):
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.FleetsApi(api).list_fleets()
        vpcloud_client.MetricsApi(api).query_metrics("c-1", QueryRequest(query="up"))
        vpcloud_client.MetricsApi(api).query_org_metrics(QueryRequest(query="up"))
        vpcloud_client.ClustersApi(api).resolve_clusters()

    harbor = [r for r in wire["requests"] if "/v1/fleets" in r["url"]]
    observatory = [r for r in wire["requests"] if "/v1/fleets" not in r["url"]]
    assert harbor[0]["url"].startswith("https://api.sea1.voltagepark.com/")
    assert harbor[0]["auth"] == f"Bearer tok[{PROD}|{HARBOR_SEA1}]"
    assert [r["url"] for r in observatory] == [OBS + "/v1/clusters/c-1/query", OBS + "/v1/query", OBS + "/v1/clusters"]
    assert {r["auth"] for r in observatory} == {f"Bearer tok[{PROD}|{OBS}]"}


def test_one_token_per_audience(wire):
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    query(config)
    query(config)
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.FleetsApi(api).list_fleets()
        vpcloud_client.FleetsApi(api).list_fleets()
    assert sorted(wire["mints"]) == sorted([(PROD, OBS), (PROD, HARBOR_SEA1)])


def test_query_text_is_sent_as_given(wire):
    query(vpcloud_client.Configuration(client_id="cid", client_secret="secret"))
    body = wire["requests"][0]["body"]
    assert (json.loads(body) if isinstance(body, str) else body) == {"query": "up"}


def test_beta_uses_the_dev_tenant(wire):
    query(vpcloud_client.Configuration(
        client_id="cid", client_secret="secret", observatory_host="https://beta.observatory.voltagepark.com"))
    assert wire["requests"][0]["url"].startswith("https://beta.observatory.voltagepark.com/")
    assert wire["mints"] == [(DEV, OBS)]


def test_regional_host_uses_the_prod_tenant(wire):
    query(vpcloud_client.Configuration(
        client_id="cid", client_secret="secret", observatory_host="https://sea1.observatory.voltagepark.com/"))
    assert wire["requests"][0]["url"] == "https://sea1.observatory.voltagepark.com/v1/clusters/c-1/query"
    assert wire["mints"] == [(PROD, OBS)]


def test_harbor_token_is_never_sent_to_observatory(wire):
    with pytest.raises(AuthenticationError):
        query(vpcloud_client.Configuration(access_token="harbor-token"))
    assert wire["requests"] == []


def test_missing_observatory_grant_names_the_audience(wire):
    wire["deny"].add(OBS)
    with pytest.raises(AuthenticationError, match="no access to https://observatory.voltagepark.com") as err:
        query(vpcloud_client.Configuration(client_id="cid", client_secret="s3cret-value"))
    assert (err.value.status_code, err.value.error, err.value.audience) == (403, "access_denied", OBS)
    assert "s3cret-value" not in str(err.value)
    assert wire["requests"] == []


def test_observatory_access_token_env(wire, monkeypatch):
    monkeypatch.setenv("VPCLOUD_OBSERVATORY_ACCESS_TOKEN", "obs-env-token")
    query(vpcloud_client.Configuration(access_token="harbor-token"))
    assert wire["requests"][0]["auth"] == "Bearer obs-env-token"


def test_responses_parse(wire):
    result = [{"metric": {"__name__": "up"}, "value": [1731100000, "1"]}]
    wire["responses"]["/v1/clusters/c-1/query"] = {
        "result": {"resultType": "vector", "resultJson": base64.b64encode(json.dumps(result).encode()).decode()}
    }
    wire["responses"]["/v1/clusters/c-1/audit/queries/q-1"] = {
        "queryId": "q-1", "state": "AUDIT_QUERY_STATE_SUCCEEDED", "statistics": {"bytesScanned": "123456789012", "eventCount": 3}
    }
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    from vpcloud_client.results import decode_result

    assert decode_result(query(config)).result == result
    with vpcloud_client.ApiClient(config) as api:
        audit = vpcloud_client.KubernetesAuditApi(api).get_audit_query("c-1", "q-1")
    assert audit.statistics.bytes_scanned == "123456789012" and audit.statistics.event_count == 3


def test_any_observatory_host_gets_the_observatory_token(wire):
    """The token follows the operation, not the host: a proxy, a private
    name or a typo still never receives the Harbor token."""
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret", observatory_host="http://localhost:8080")
    query(config)
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.FleetsApi(api).list_fleets()
    observatory = [r for r in wire["requests"] if r["url"].startswith("http://localhost:8080/")]
    harbor = [r for r in wire["requests"] if "/v1/fleets" in r["url"]]
    assert [r["auth"] for r in observatory] == [f"Bearer tok[{PROD}|{OBS}]"]
    assert harbor[0]["auth"] == f"Bearer tok[{PROD}|{HARBOR_SEA1}]"


def test_ignore_operation_servers_redirects_only_harbor(wire):
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret", host="https://harbor.example")
    config.ignore_operation_servers = True
    query(config)
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.FleetsApi(api).list_fleets()
    assert wire["requests"][0]["url"] == OBS + "/v1/clusters/c-1/query"
    assert wire["requests"][1]["url"] == "https://harbor.example/v1/fleets"


def test_observatory_auth0_domain_override(wire):
    query(vpcloud_client.Configuration(
        client_id="cid", client_secret="secret", observatory_host="https://observatory.internal.example",
        observatory_auth0_domain=DEV))
    assert wire["mints"] == [(DEV, OBS)]


def test_short_lived_token_is_reused(wire):
    wire["expires_in"] = 120  # shorter than the 5-minute refresh margin
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    query(config)
    query(config)
    assert wire["mints"] == [(PROD, OBS)]


def test_absent_booleans_read_as_false(wire):
    """proto3 JSON omits a false boolean, so an untruncated result has no
    `truncated` at all."""
    wire["responses"]["/v1/clusters/c-1/audit/queries/q-1"] = {"queryId": "q-1", "statistics": {"eventCount": 3}}
    wire["responses"]["/v1/clusters/c-1/audit/queries/q-1/results"] = {"eventsJson": []}
    wire["responses"]["/v1/clusters"] = {"clusters": [{"clusterId": "c-1"}]}
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    with vpcloud_client.ApiClient(config) as api:
        audit = vpcloud_client.KubernetesAuditApi(api)
        assert audit.get_audit_query("c-1", "q-1").statistics.truncated is False
        assert audit.get_audit_query_results("c-1", "q-1").truncated is False
        cluster = vpcloud_client.ClustersApi(api).resolve_clusters().clusters[0]
    assert (cluster.metrics_ready, cluster.logs_ready) == (False, False)
    wire["responses"]["/v1/clusters/c-1/audit/queries/q-1"] = {"queryId": "q-1", "statistics": {"truncated": True}}
    with vpcloud_client.ApiClient(config) as api:
        assert vpcloud_client.KubernetesAuditApi(api).get_audit_query("c-1", "q-1").statistics.truncated is True


def list_fleets(config):
    with vpcloud_client.ApiClient(config) as api:
        return vpcloud_client.FleetsApi(api).list_fleets()


def test_region_without_a_grant_raises_before_any_request(wire):
    """An application granted only another region's API is refused by Auth0;
    the call raises naming the audience and the fix, instead of sending the
    request without a token and failing with a bare 401."""
    wire["deny"].add(HARBOR_SEA1)
    with pytest.raises(AuthenticationError) as err:
        list_fleets(vpcloud_client.Configuration(client_id="cid", client_secret="s3cret-value"))
    message = str(err.value)
    assert message.startswith(f"This client has no access to {HARBOR_SEA1}. Set Configuration(host=...)")
    assert "https://api.iad1.voltagepark.com" in message
    assert "https://api.sea1.voltagepark.com" not in message  # the host that was refused
    assert "s3cret-value" not in message
    assert (err.value.status_code, err.value.error, err.value.audience) == (403, "access_denied", HARBOR_SEA1)
    assert wire["requests"] == []


def test_granted_region_host_works(wire):
    wire["deny"].add(HARBOR_SEA1)
    list_fleets(vpcloud_client.Configuration(client_id="cid", client_secret="secret", host="https://api.iad1.voltagepark.com"))
    assert wire["requests"][0]["url"] == "https://api.iad1.voltagepark.com/v1/fleets"
    assert wire["requests"][0]["auth"] == f"Bearer tok[{PROD}|https://api.iad-1.voltagepark.com/harbor]"


def test_rejected_client_secret_says_so(wire):
    wire["bad_secret"] = True
    with pytest.raises(AuthenticationError, match="rejected the client credentials") as err:
        list_fleets(vpcloud_client.Configuration(client_id="cid", client_secret="s3cret-value"))
    assert err.value.status_code == 401
    assert "s3cret-value" not in str(err.value)
    with pytest.raises(AuthenticationError, match="rejected the client credentials"):
        query(vpcloud_client.Configuration(client_id="cid", client_secret="s3cret-value"))
    assert wire["requests"] == []


def test_refused_exchange_falls_back_to_the_credentials_file_token(wire, monkeypatch, tmp_path):
    creds = tmp_path / "credentials"
    creds.write_text("[default]\naccess_token = file-token\n")
    monkeypatch.setattr(credentials.CredentialProvider, "CREDENTIALS_FILE", creds)
    wire["deny"].add(HARBOR_SEA1)
    list_fleets(vpcloud_client.Configuration(client_id="cid", client_secret="secret"))
    assert wire["requests"][0]["auth"] == "Bearer file-token"


def test_configs_without_client_credentials_are_unchanged(wire):
    list_fleets(vpcloud_client.Configuration(access_token="harbor-token"))
    list_fleets(vpcloud_client.Configuration())
    assert wire["mints"] == []
    assert [r["auth"] for r in wire["requests"]] == ["Bearer harbor-token", None]
