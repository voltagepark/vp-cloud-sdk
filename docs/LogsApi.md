# vpcloud_client.LogsApi

All URIs are relative to *https://api.sea1.voltagepark.com*

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
import vpcloud_client
from vpcloud_client.models.logs_query_request import LogsQueryRequest
from vpcloud_client.models.observatory_v1_logs_query_response import ObservatoryV1LogsQueryResponse
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
    api_instance = vpcloud_client.LogsApi(api_client)
    cluster_id = 'cluster_id_example' # str | A cluster your organization owns.
    logs_query_request = vpcloud_client.LogsQueryRequest() # LogsQueryRequest | 

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

