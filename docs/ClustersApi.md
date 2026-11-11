# vpcloud_client.ClustersApi

All URIs are relative to *https://api.sea1.voltagepark.com*

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
import vpcloud_client
from vpcloud_client.models.observatory_v1_resolve_clusters_response import ObservatoryV1ResolveClustersResponse
from vpcloud_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.sea1.voltagepark.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vpcloud_client.Configuration(
    host = "https://api.sea1.voltagepark.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = vpcloud_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
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

