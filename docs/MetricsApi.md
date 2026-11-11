# vpcloud_client.MetricsApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**query_metrics**](MetricsApi.md#query_metrics) | **POST** /v1/clusters/{cluster_id}/query | Run an instant PromQL query
[**query_metrics_range**](MetricsApi.md#query_metrics_range) | **POST** /v1/clusters/{cluster_id}/query_range | Run a range PromQL query
[**query_org_metrics**](MetricsApi.md#query_org_metrics) | **POST** /v1/query | Run an instant PromQL query across your organization
[**query_org_metrics_range**](MetricsApi.md#query_org_metrics_range) | **POST** /v1/query_range | Run a range PromQL query across your organization


# **query_metrics**
> ObservatoryV1QueryResponse query_metrics(cluster_id, query_request)

Run an instant PromQL query

Evaluates a PromQL query over one cluster's metrics at a single point in time. The result is in Prometheus format.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.observatory_v1_query_response import ObservatoryV1QueryResponse
from vpcloud_client.models.query_request import QueryRequest
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
    api_instance = vpcloud_client.MetricsApi(api_client)
    cluster_id = 'cluster_id_example' # str | A cluster your organization owns.
    query_request = vpcloud_client.QueryRequest() # QueryRequest | 

    try:
        # Run an instant PromQL query
        api_response = api_instance.query_metrics(cluster_id, query_request)
        print("The response of MetricsApi->query_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->query_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| A cluster your organization owns. | 
 **query_request** | [**QueryRequest**](QueryRequest.md)|  | 

### Return type

[**ObservatoryV1QueryResponse**](ObservatoryV1QueryResponse.md)

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

# **query_metrics_range**
> ObservatoryV1QueryRangeResponse query_metrics_range(cluster_id, query_range_request)

Run a range PromQL query

Evaluates a PromQL query over one cluster's metrics across a time range, at a fixed step. The result is in Prometheus format.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.observatory_v1_query_range_response import ObservatoryV1QueryRangeResponse
from vpcloud_client.models.query_range_request import QueryRangeRequest
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
    api_instance = vpcloud_client.MetricsApi(api_client)
    cluster_id = 'cluster_id_example' # str | A cluster your organization owns.
    query_range_request = vpcloud_client.QueryRangeRequest() # QueryRangeRequest | 

    try:
        # Run a range PromQL query
        api_response = api_instance.query_metrics_range(cluster_id, query_range_request)
        print("The response of MetricsApi->query_metrics_range:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->query_metrics_range: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| A cluster your organization owns. | 
 **query_range_request** | [**QueryRangeRequest**](QueryRangeRequest.md)|  | 

### Return type

[**ObservatoryV1QueryRangeResponse**](ObservatoryV1QueryRangeResponse.md)

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

# **query_org_metrics**
> ObservatoryV1QueryResponse query_org_metrics(query_request)

Run an instant PromQL query across your organization

Evaluates a PromQL query over all of your organization's metrics, including metrics not tied to a single cluster, at a single point in time. The result is in Prometheus format.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.observatory_v1_query_response import ObservatoryV1QueryResponse
from vpcloud_client.models.query_request import QueryRequest
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
    api_instance = vpcloud_client.MetricsApi(api_client)
    query_request = vpcloud_client.QueryRequest() # QueryRequest | 

    try:
        # Run an instant PromQL query across your organization
        api_response = api_instance.query_org_metrics(query_request)
        print("The response of MetricsApi->query_org_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->query_org_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_request** | [**QueryRequest**](QueryRequest.md)|  | 

### Return type

[**ObservatoryV1QueryResponse**](ObservatoryV1QueryResponse.md)

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

# **query_org_metrics_range**
> ObservatoryV1QueryRangeResponse query_org_metrics_range(query_range_request)

Run a range PromQL query across your organization

Evaluates a PromQL query over all of your organization's metrics across a time range, at a fixed step. The result is in Prometheus format.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.observatory_v1_query_range_response import ObservatoryV1QueryRangeResponse
from vpcloud_client.models.query_range_request import QueryRangeRequest
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
    api_instance = vpcloud_client.MetricsApi(api_client)
    query_range_request = vpcloud_client.QueryRangeRequest() # QueryRangeRequest | 

    try:
        # Run a range PromQL query across your organization
        api_response = api_instance.query_org_metrics_range(query_range_request)
        print("The response of MetricsApi->query_org_metrics_range:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->query_org_metrics_range: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_range_request** | [**QueryRangeRequest**](QueryRangeRequest.md)|  | 

### Return type

[**ObservatoryV1QueryRangeResponse**](ObservatoryV1QueryRangeResponse.md)

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

