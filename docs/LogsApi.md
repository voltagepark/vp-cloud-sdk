# vpcloud_client.LogsApi

All URIs are relative to *https://observatory.voltagepark.com*, the default `Configuration.observatory_host`. `ClustersApi.resolve_clusters()` reports the regional endpoint that serves each cluster.

Method | HTTP request | Description
------------- | ------------- | -------------
[**query_logs**](LogsApi.md#query_logs) | **POST** /v1/clusters/{cluster_id}/logs/query | Query logs


# **query_logs**
> ObservatoryV1LogsQueryResponse query_logs(cluster_id, logs_query_request)

Query logs

Runs a LogsQL query over one cluster's logs and returns the matching lines.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import datetime
import os
import vpcloud_client
from vpcloud_client.models.logs_query_request import LogsQueryRequest
from vpcloud_client.models.observatory_v1_logs_query_response import ObservatoryV1LogsQueryResponse
from vpcloud_client.rest import ApiException
from pprint import pprint

# Observatory operations (metrics, logs, audit) are sent to observatory_host,
# https://observatory.voltagepark.com by default. ClustersApi.resolve_clusters()
# reports the regional endpoint that serves each cluster; set observatory_host
# to it for a cluster served elsewhere.
# The SDK exchanges your application's client credentials for an access token.
# See configuration.py for a list of all supported configuration parameters.
configuration = vpcloud_client.Configuration(
    observatory_host = "https://observatory.voltagepark.com",
    client_id = os.environ["VPCLOUD_CLIENT_ID"],
    client_secret = os.environ["VPCLOUD_CLIENT_SECRET"],
)

# Enter a context with an instance of the API client
with vpcloud_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vpcloud_client.LogsApi(api_client)
    now = datetime.datetime.now(datetime.timezone.utc)
    cluster_id = 'cluster_id_example' # str | A cluster your organization owns.
    logs_query_request = vpcloud_client.LogsQueryRequest(query='error', start=now - datetime.timedelta(hours=1), end=now, limit=100) # LogsQueryRequest | 

    try:
        # Query logs
        api_response = api_instance.query_logs(cluster_id, logs_query_request)
        print("The response of LogsApi->query_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LogsApi->query_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| A cluster your organization owns. | 
 **logs_query_request** | [**LogsQueryRequest**](LogsQueryRequest.md)|  | 

### Return type

[**ObservatoryV1LogsQueryResponse**](ObservatoryV1LogsQueryResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

