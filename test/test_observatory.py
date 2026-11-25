# coding: utf-8

"""Routing and credential tests for the Observatory APIs (metrics, logs,
audit). Auth0 and the HTTP layer are faked; every assertion is on what the SDK
would have sent. No network."""

import base64
import datetime
import json

import httpx
import pytest
import urllib3

import vpcloud_client
from vpcloud_client import credentials, rest
from vpcloud_client.credentials import AuthenticationError
from vpcloud_client.models.logs_query_request import LogsQueryRequest
from vpcloud_client.models.query_range_request import QueryRangeRequest
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
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(credentials.CredentialProvider, "CREDENTIALS_FILE", tmp_path / "credentials")
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
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret", region="sea1")
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.FleetsApi(api).list_fleets()
        vpcloud_client.MetricsApi(api).query_metrics("c-1", QueryRequest(query="up"))
        vpcloud_client.MetricsApi(api).query_org_metrics(QueryRequest(query="up"))
        vpcloud_client.ClustersApi(api).resolve_clusters()

    harbor = [r for r in wire["requests"] if "/v1/fleets" in r["url"]]
    observatory = [r for r in wire["requests"] if "/v1/fleets" not in r["url"]]
    assert harbor[0]["url"].startswith("https://api.sea1.voltagepark.com/")
    assert harbor[0]["auth"] == f"Bearer tok[{PROD}|{HARBOR_SEA1}]"
    assert [r["url"] for r in observatory] == [
        SEA1_OBS + "/v1/clusters/c-1/query",
        OBS + "/v1/query",
        SEA1_OBS + "/v1/clusters",
    ]
    assert {r["auth"] for r in observatory} == {f"Bearer tok[{PROD}|{OBS}]"}


def test_one_token_per_audience(wire):
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret", region="sea1")
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


@pytest.mark.parametrize("step", ["5m", 300, datetime.timedelta(minutes=5)])
def test_range_query_step_is_sent_in_seconds(wire, step):
    """The gateway takes a protobuf Duration ("300s") and answers "5m" with an error."""
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    end = datetime.datetime(2026, 11, 23, tzinfo=datetime.timezone.utc)
    request = QueryRangeRequest(query="up", start=end - datetime.timedelta(hours=1), end=end, step=step)
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.MetricsApi(api).query_metrics_range("c-1", request)
        vpcloud_client.MetricsApi(api).query_org_metrics_range(request)
    bodies = [r["body"] for r in wire["requests"]]
    assert [r["url"] for r in wire["requests"]] == [OBS + "/v1/clusters/c-1/query_range", OBS + "/v1/query_range"]
    assert [(json.loads(b) if isinstance(b, str) else b)["step"] for b in bodies] == ["300s", "300s"]


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
    config = vpcloud_client.Configuration(
        client_id="cid", client_secret="secret", region="sea1", observatory_host="http://localhost:8080")
    query(config)
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.FleetsApi(api).list_fleets()
    observatory = [r for r in wire["requests"] if r["url"].startswith("http://localhost:8080/")]
    harbor = [r for r in wire["requests"] if "/v1/fleets" in r["url"]]
    assert [r["auth"] for r in observatory] == [f"Bearer tok[{PROD}|{OBS}]"]
    assert harbor[0]["auth"] == f"Bearer tok[{PROD}|{HARBOR_SEA1}]"


def test_ignore_operation_servers_redirects_only_harbor(wire):
    config = vpcloud_client.Configuration(
        client_id="cid", client_secret="secret", host="https://harbor.example", region="sea1"
    )
    config.ignore_operation_servers = True
    query(config)
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.FleetsApi(api).list_fleets()
    assert wire["requests"][0]["url"] == SEA1_OBS + "/v1/clusters/c-1/query"
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


@pytest.mark.parametrize("region,host,audience", [
    ("sea1", "https://api.sea1.voltagepark.com", "https://api.sea-1.voltagepark.com/harbor"),
    ("iad1", "https://api.iad1.voltagepark.com", "https://api.iad-1.voltagepark.com/harbor"),
    ("dfw2", "https://api.dfw2.voltagepark.com", "https://api.dfw-2.voltagepark.com/harbor"),
    ("ord1", "https://api.ord1.voltagepark.com", "https://api.ord-1.voltagepark.com/harbor"),
])
def test_region_sets_host_and_audience(wire, region, host, audience):
    list_fleets(vpcloud_client.Configuration(client_id="cid", client_secret="secret", region=region))
    assert wire["requests"][0]["url"] == host + "/v1/fleets"
    assert wire["mints"] == [(PROD, audience)]


def test_region_from_env(wire, monkeypatch):
    monkeypatch.setenv("VPCLOUD_REGION", " IAD1 ")
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    list_fleets(config)
    assert config.region == "iad1"
    assert wire["requests"][0]["url"] == "https://api.iad1.voltagepark.com/v1/fleets"


def test_region_from_credentials_profile(wire, tmp_path):
    (tmp_path / "credentials").write_text("[default]\nregion = ord1\n[other]\nregion = dfw2\n")
    assert vpcloud_client.Configuration().region == "ord1"
    assert vpcloud_client.Configuration(profile="other").region == "dfw2"


def test_region_precedence_is_argument_then_env_then_file(wire, monkeypatch, tmp_path):
    (tmp_path / "credentials").write_text("[default]\nregion = ord1\n")
    monkeypatch.setenv("VPCLOUD_REGION", "iad1")
    explicit = vpcloud_client.Configuration(region="dfw2")
    from_env = vpcloud_client.Configuration()
    assert explicit.region == "dfw2"
    assert from_env.region == "iad1"
    assert explicit._credential_provider._credentials_cache is None
    assert from_env._credential_provider._credentials_cache is None


def test_missing_region_fails_before_any_request(wire):
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    with pytest.raises(ValueError, match="No region set.*VPCLOUD_REGION.*sea1, iad1, dfw2, ord1"):
        list_fleets(config)
    with pytest.raises(ValueError, match="No region set.*VPCLOUD_REGION.*sea1, iad1, dfw2, ord1"):
        with vpcloud_client.ApiClient(config) as api:
            vpcloud_client.AuditApi(api).get_audit_logs()
    assert wire["requests"] == [] and wire["mints"] == []


def test_observatory_needs_no_region(wire):
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.MetricsApi(api).query_metrics("c-1", QueryRequest(query="up"))
        vpcloud_client.LogsApi(api).query_logs("c-1", LogsQueryRequest(query="error"))
        vpcloud_client.KubernetesAuditApi(api).get_audit_coverage("c-1")
        vpcloud_client.ClustersApi(api).resolve_clusters()
    assert config.region is None
    assert [r["url"] for r in wire["requests"]] == [
        OBS + "/v1/clusters/c-1/query",
        OBS + "/v1/clusters/c-1/logs/query",
        OBS + "/v1/clusters/c-1/audit/coverage",
        OBS + "/v1/clusters",
    ]


def test_unknown_region_lists_valid_regions(wire, monkeypatch, tmp_path):
    with pytest.raises(ValueError, match=r"Unknown region 'us-east-1' \(from region\).*sea1, iad1, dfw2, ord1"):
        vpcloud_client.Configuration(region="us-east-1")
    monkeypatch.setenv("VPCLOUD_REGION", "sea-1")
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret")
    with pytest.raises(ValueError, match=r"from VPCLOUD_REGION"):
        list_fleets(config)
    monkeypatch.delenv("VPCLOUD_REGION")
    (tmp_path / "credentials").write_text("[default]\nregion = eu-west-1\n")
    with pytest.raises(ValueError, match=r"from credentials profile 'default'"):
        vpcloud_client.Configuration().region
    assert wire["requests"] == [] and wire["mints"] == []


def test_bad_env_region_does_not_break_observatory(wire, monkeypatch):
    monkeypatch.setenv("VPCLOUD_REGION", "iad-1")
    config = vpcloud_client.Configuration(observatory_access_token="obs-jwt")
    query(config)
    assert wire["requests"][0]["auth"] == "Bearer obs-jwt"


def test_region_with_host_picks_the_audience(wire):
    config = vpcloud_client.Configuration(
        client_id="cid", client_secret="secret", region="iad1", host="https://harbor-proxy.internal"
    )
    list_fleets(config)
    assert wire["requests"][0]["url"] == "https://harbor-proxy.internal/v1/fleets"
    assert wire["mints"] == [(PROD, "https://api.iad-1.voltagepark.com/harbor")]
    with pytest.raises(ValueError, match="region or server_index, not both"):
        vpcloud_client.Configuration(region="iad1", server_index=0)


@pytest.mark.parametrize("host", ["https://harbor-proxy.internal", "https://api.beta.iad1.voltagepark.com"])
def test_unrecognized_host_without_region_raises(wire, host):
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret", host=host)
    with pytest.raises(ValueError, match="Can't tell which region .* serves; pass region= with host="):
        list_fleets(config)
    assert wire["requests"] == [] and wire["mints"] == []


def test_explicit_host_ignores_env_region(wire, monkeypatch):
    monkeypatch.setenv("VPCLOUD_REGION", "not-a-region")
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret", host="https://api.dfw2.voltagepark.com")
    list_fleets(config)
    assert config.region is None
    assert wire["mints"] == [(PROD, "https://api.dfw-2.voltagepark.com/harbor")]


def test_uppercase_host_derives_audience_and_ignores_lookalike(wire):
    config = vpcloud_client.Configuration(
        client_id="cid", client_secret="secret", host="https://API.DFW2.VOLTAGEPARK.COM"
    )
    list_fleets(config)
    assert wire["mints"] == [(PROD, "https://api.dfw-2.voltagepark.com/harbor")]
    assert credentials.Auth0TokenManager.region_for_host("https://api.iad1.voltagepark.com.evil.example") is None


def test_region_can_change_after_construction(wire):
    config = vpcloud_client.Configuration(client_id="cid", client_secret="secret", region="sea1")
    list_fleets(config)
    config.region = "ord1"
    assert config.access_token is None
    list_fleets(config)
    assert [r["url"] for r in wire["requests"]] == [
        "https://api.sea1.voltagepark.com/v1/fleets",
        "https://api.ord1.voltagepark.com/v1/fleets",
    ]
    assert wire["mints"] == [
        (PROD, HARBOR_SEA1),
        (PROD, "https://api.ord-1.voltagepark.com/harbor"),
    ]
    config.server_index = 1
    assert config.region is None
    assert config.host == "https://api.iad1.voltagepark.com"
    config.host = "https://harbor.example"
    assert config.region == "ord1"


def test_access_token_assigned_after_construction_keeps_region(wire):
    config = vpcloud_client.Configuration(region="iad1")
    config.access_token = "direct-jwt"
    list_fleets(config)
    assert wire["requests"][0]["url"] == "https://api.iad1.voltagepark.com/v1/fleets"
    assert wire["requests"][0]["auth"] == "Bearer direct-jwt"
    assert wire["mints"] == []


def test_region_without_a_grant_raises_before_any_request(wire):
    """An application granted only another region's API is refused by Auth0;
    the call raises naming the region and audience instead of sending the
    request without a token and failing with a bare 401."""
    iad1 = "https://api.iad-1.voltagepark.com/harbor"
    wire["deny"].add(iad1)
    config = vpcloud_client.Configuration(client_id="cid", client_secret="s3cret-value", region="iad1")
    with pytest.raises(AuthenticationError) as err:
        list_fleets(config)
    message = str(err.value)
    assert message.startswith(f"This client has no access to {iad1} (region iad1). Check that iad1")
    assert "s3cret-value" not in message
    assert (err.value.status_code, err.value.error, err.value.audience) == (403, "access_denied", iad1)
    assert wire["requests"] == []


def test_rejected_client_secret_says_so(wire):
    wire["bad_secret"] = True
    with pytest.raises(AuthenticationError, match="rejected the client credentials") as err:
        list_fleets(vpcloud_client.Configuration(client_id="cid", client_secret="s3cret-value", region="sea1"))
    assert err.value.status_code == 401
    assert "s3cret-value" not in str(err.value)
    with pytest.raises(AuthenticationError, match="rejected the client credentials"):
        query(vpcloud_client.Configuration(client_id="cid", client_secret="s3cret-value"))
    assert wire["requests"] == []


def test_refused_exchange_does_not_fall_back_to_the_credentials_file_token(wire, tmp_path):
    (tmp_path / "credentials").write_text("[default]\naccess_token = file-token\n")
    wire["deny"].add(HARBOR_SEA1)
    with pytest.raises(AuthenticationError, match="region sea1"):
        list_fleets(vpcloud_client.Configuration(client_id="cid", client_secret="secret", region="sea1"))
    assert wire["requests"] == []


def test_configs_without_client_credentials_are_unchanged(wire):
    list_fleets(vpcloud_client.Configuration(access_token="harbor-token", region="sea1"))
    list_fleets(vpcloud_client.Configuration(region="sea1"))
    assert wire["mints"] == []
    assert [r["auth"] for r in wire["requests"]] == ["Bearer harbor-token", None]


ORD1_OBS = "https://ord1.observatory.voltagepark.com"
SEA1_OBS = "https://sea1.observatory.voltagepark.com"
DFW2_OBS = "https://dfw2.observatory.voltagepark.com"


def obs_config(**kwargs):
    return vpcloud_client.Configuration(client_id="cid", client_secret="secret", **kwargs)


def observatory_urls(wire, config):
    """Send one of each kind of Observatory call and return their URLs:
    per-cluster metrics, logs and audit, resolve_clusters, then org-wide metrics."""
    end = datetime.datetime(2026, 11, 23, tzinfo=datetime.timezone.utc)
    sent = len(wire["requests"])
    with vpcloud_client.ApiClient(config) as api:
        vpcloud_client.MetricsApi(api).query_metrics("c-1", QueryRequest(query="up"))
        vpcloud_client.LogsApi(api).query_logs("c-1", LogsQueryRequest(query="error"))
        vpcloud_client.KubernetesAuditApi(api).get_audit_coverage("c-1")
        vpcloud_client.ClustersApi(api).resolve_clusters()
        vpcloud_client.MetricsApi(api).query_org_metrics(QueryRequest(query="up"))
        vpcloud_client.MetricsApi(api).query_org_metrics_range(QueryRangeRequest(
            query="up", start=end - datetime.timedelta(hours=1), end=end, step="60s"))
    return [r["url"] for r in wire["requests"][sent:]]


def routed(per_cluster, org_wide):
    return [
        per_cluster + "/v1/clusters/c-1/query",
        per_cluster + "/v1/clusters/c-1/logs/query",
        per_cluster + "/v1/clusters/c-1/audit/coverage",
        per_cluster + "/v1/clusters",
        org_wide + "/v1/query",
        org_wide + "/v1/query_range",
    ]


@pytest.mark.parametrize("arg,env,region,expected", [
    ("https://arg.example", "https://env.example", "ord1", "https://arg.example"),
    (None, "https://env.example", "ord1", "https://env.example"),
    (None, None, "ord1", ORD1_OBS),
    (None, None, None, OBS),
])
def test_observatory_host_precedence_is_argument_env_region_default(wire, monkeypatch, arg, env, region, expected):
    if env:
        monkeypatch.setenv("VPCLOUD_OBSERVATORY_HOST", env)
    config = obs_config(observatory_host=arg, region=region)
    assert observatory_urls(wire, config) == routed(expected, expected)


@pytest.mark.parametrize("region,per_cluster,org_wide", [
    ("ord1", ORD1_OBS, ORD1_OBS),
    ("iad1", OBS, OBS),
    ("sea1", SEA1_OBS, OBS),
    ("dfw2", DFW2_OBS, OBS),
])
def test_region_picks_the_observability_endpoint(wire, region, per_cluster, org_wide):
    """iad1's endpoint is the default one; sea1 and dfw2 send org-wide metrics there."""
    assert observatory_urls(wire, obs_config(region=region)) == routed(per_cluster, org_wide)


def test_one_observatory_token_for_every_regional_endpoint(wire):
    config = obs_config(region="ord1")
    observatory_urls(wire, config)
    config.region = "iad1"
    observatory_urls(wire, config)
    assert wire["mints"] == [(PROD, OBS)]
    assert {r["auth"] for r in wire["requests"]} == {f"Bearer tok[{PROD}|{OBS}]"}


def test_env_and_credentials_file_region_pick_the_observability_endpoint(wire, monkeypatch, tmp_path):
    monkeypatch.setenv("VPCLOUD_REGION", " ORD1 ")
    assert obs_config().observatory_host == ORD1_OBS
    monkeypatch.delenv("VPCLOUD_REGION")
    (tmp_path / "credentials").write_text("[default]\nregion = ord1\n")
    assert observatory_urls(wire, obs_config()) == routed(ORD1_OBS, ORD1_OBS)


@pytest.mark.parametrize("source", ["env", "file"])
def test_unknown_env_or_file_region_uses_the_default_endpoint(wire, monkeypatch, tmp_path, source):
    if source == "env":
        monkeypatch.setenv("VPCLOUD_REGION", "ord-1")
    else:
        (tmp_path / "credentials").write_text("[default]\nregion = eu-west-1\n")
    config = obs_config()
    assert observatory_urls(wire, config) == routed(OBS, OBS)
    assert wire["mints"] == [(PROD, OBS)]
    with pytest.raises(ValueError, match="Unknown region"):
        config.region


def test_org_wide_host_skips_a_regional_endpoint_without_org_metrics(wire):
    config = obs_config(region="sea1")
    assert (config.observatory_host, config.observatory_org_host) == (SEA1_OBS, OBS)


@pytest.mark.parametrize("region,override", [
    ("ord1", "https://observatory.voltagepark.com/"),
    ("sea1", "https://proxy.example/"),
])
def test_explicit_observatory_host_wins_for_every_call(wire, region, override):
    config = obs_config(region=region, observatory_host=override)
    expected = override.rstrip("/")
    assert observatory_urls(wire, config) == routed(expected, expected)


def test_observatory_host_follows_later_changes(wire):
    config = obs_config(region="sea1")
    assert config.observatory_host == SEA1_OBS
    config.region = "ord1"
    assert (config.observatory_host, config.observatory_org_host) == (ORD1_OBS, ORD1_OBS)
    config.observatory_host = "https://proxy.example/"
    assert (config.observatory_host, config.observatory_org_host) == ("https://proxy.example", "https://proxy.example")
    config.observatory_host = None
    assert config.observatory_host == ORD1_OBS
    config.server_index = 1
    assert config.observatory_host == OBS


def test_regional_api_host_picks_the_observability_endpoint(wire, monkeypatch):
    monkeypatch.setenv("VPCLOUD_REGION", "iad1")
    assert obs_config(host="https://api.ord1.voltagepark.com").observatory_host == ORD1_OBS
    assert obs_config(host="https://harbor-proxy.internal").observatory_host == OBS


def test_beta_endpoint_keeps_the_dev_tenant_with_a_region(wire):
    beta = "https://beta.observatory.voltagepark.com"
    assert observatory_urls(wire, obs_config(region="ord1", observatory_host=beta)) == routed(beta, beta)
    assert wire["mints"] == [(DEV, OBS)]
