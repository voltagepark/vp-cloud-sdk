# vpcloud_client.ClustersApi

Per-cluster URIs and `ClustersApi` URIs are relative to `Configuration.observatory_host`: *https://&lt;region&gt;.observatory.voltagepark.com* for sea1, dfw2 and ord1, else *https://observatory.voltagepark.com*. Org-wide `MetricsApi` URIs use `Configuration.observatory_org_host`, which stays on the main host for sea1 and dfw2. `ClustersApi.resolve_clusters()` reports the regional endpoint that serves each cluster. These APIs don't need a region, and an unknown one doesn't break them.

Method | HTTP request | Description
------------- | ------------- | -------------
[**resolve_clusters**](ClustersApi.md#resolve_clusters) | **GET** /v1/clusters | List your clusters


# **resolve_clusters**
> ObservatoryV1ResolveClustersResponse resolve_clusters()

List your clusters

Lists the clusters your organization owns, the regional endpoint that serves each one, and whether its metrics and logs can be queried yet.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import os
import vpcloud_client
from vpcloud_client.models.observatory_v1_resolve_clusters_response import ObservatoryV1ResolveClustersResponse
from vpcloud_client.rest import ApiException
from pprint import pprint

# Uses VPCLOUD_REGION's Observability endpoint (main host for sea1/dfw2 org metrics); set observatory_host to override.
# The SDK exchanges your application's client credentials for an access token.
# See configuration.py for a list of all supported configuration parameters.
configuration = vpcloud_client.Configuration(
    client_id = os.environ["VPCLOUD_CLIENT_ID"],
    client_secret = os.environ["VPCLOUD_CLIENT_SECRET"],
)

# Enter a context with an instance of the API client
with vpcloud_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vpcloud_client.ClustersApi(api_client)

    try:
        # List your clusters
        api_response = api_instance.resolve_clusters()
        print("The response of ClustersApi->resolve_clusters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClustersApi->resolve_clusters: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ObservatoryV1ResolveClustersResponse**](ObservatoryV1ResolveClustersResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

