# vpcloud_client.KubernetesAuditApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_audit_query**](KubernetesAuditApi.md#cancel_audit_query) | **POST** /v1/clusters/{cluster_id}/audit/queries/{query_id}/cancel | Cancel an audit log query
[**create_audit_query**](KubernetesAuditApi.md#create_audit_query) | **POST** /v1/clusters/{cluster_id}/audit/queries | Start an audit log query
[**get_audit_coverage**](KubernetesAuditApi.md#get_audit_coverage) | **GET** /v1/clusters/{cluster_id}/audit/coverage | Get audit log coverage
[**get_audit_query**](KubernetesAuditApi.md#get_audit_query) | **GET** /v1/clusters/{cluster_id}/audit/queries/{query_id} | Get an audit log query
[**get_audit_query_results**](KubernetesAuditApi.md#get_audit_query_results) | **GET** /v1/clusters/{cluster_id}/audit/queries/{query_id}/results | Read audit log query results


# **cancel_audit_query**
> ObservatoryV1CancelAuditQueryResponse cancel_audit_query(cluster_id, query_id)

Cancel an audit log query

Stops a queued or running query.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.observatory_v1_cancel_audit_query_response import ObservatoryV1CancelAuditQueryResponse
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
    api_instance = vpcloud_client.KubernetesAuditApi(api_client)
    cluster_id = 'cluster_id_example' # str | A cluster your organization owns.
    query_id = 'query_id_example' # str | The queryId that createAuditQuery returned.

    try:
        # Cancel an audit log query
        api_response = api_instance.cancel_audit_query(cluster_id, query_id)
        print("The response of KubernetesAuditApi->cancel_audit_query:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesAuditApi->cancel_audit_query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| A cluster your organization owns. | 
 **query_id** | **str**| The queryId that createAuditQuery returned. | 

### Return type

[**ObservatoryV1CancelAuditQueryResponse**](ObservatoryV1CancelAuditQueryResponse.md)

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

# **create_audit_query**
> ObservatoryV1CreateAuditQueryResponse create_audit_query(cluster_id, create_audit_query_request)

Start an audit log query

Starts a query over the cluster's Kubernetes audit log. Queries run asynchronously: poll getAuditQuery until the query has finished, then page through its events with getAuditQueryResults. Sending the same requestId again returns the same query.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.create_audit_query_request import CreateAuditQueryRequest
from vpcloud_client.models.observatory_v1_create_audit_query_response import ObservatoryV1CreateAuditQueryResponse
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
    api_instance = vpcloud_client.KubernetesAuditApi(api_client)
    cluster_id = 'cluster_id_example' # str | A cluster your organization owns.
    create_audit_query_request = vpcloud_client.CreateAuditQueryRequest() # CreateAuditQueryRequest | 

    try:
        # Start an audit log query
        api_response = api_instance.create_audit_query(cluster_id, create_audit_query_request)
        print("The response of KubernetesAuditApi->create_audit_query:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesAuditApi->create_audit_query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| A cluster your organization owns. | 
 **create_audit_query_request** | [**CreateAuditQueryRequest**](CreateAuditQueryRequest.md)|  | 

### Return type

[**ObservatoryV1CreateAuditQueryResponse**](ObservatoryV1CreateAuditQueryResponse.md)

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

# **get_audit_coverage**
> ObservatoryV1GetAuditCoverageResponse get_audit_coverage(cluster_id)

Get audit log coverage

Reports the time span the cluster's Kubernetes audit log covers, and any known gaps in it.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.observatory_v1_get_audit_coverage_response import ObservatoryV1GetAuditCoverageResponse
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
    api_instance = vpcloud_client.KubernetesAuditApi(api_client)
    cluster_id = 'cluster_id_example' # str | A cluster your organization owns.

    try:
        # Get audit log coverage
        api_response = api_instance.get_audit_coverage(cluster_id)
        print("The response of KubernetesAuditApi->get_audit_coverage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesAuditApi->get_audit_coverage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| A cluster your organization owns. | 

### Return type

[**ObservatoryV1GetAuditCoverageResponse**](ObservatoryV1GetAuditCoverageResponse.md)

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

# **get_audit_query**
> ObservatoryV1GetAuditQueryResponse get_audit_query(cluster_id, query_id, wait_seconds=wait_seconds)

Get an audit log query

Returns the query's state, statistics and coverage.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.observatory_v1_get_audit_query_response import ObservatoryV1GetAuditQueryResponse
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
    api_instance = vpcloud_client.KubernetesAuditApi(api_client)
    cluster_id = 'cluster_id_example' # str | A cluster your organization owns.
    query_id = 'query_id_example' # str | The queryId that createAuditQuery returned.
    wait_seconds = 56 # int | Seconds to wait for the query to change state before answering, up to 20. (optional)

    try:
        # Get an audit log query
        api_response = api_instance.get_audit_query(cluster_id, query_id, wait_seconds=wait_seconds)
        print("The response of KubernetesAuditApi->get_audit_query:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesAuditApi->get_audit_query: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| A cluster your organization owns. | 
 **query_id** | **str**| The queryId that createAuditQuery returned. | 
 **wait_seconds** | **int**| Seconds to wait for the query to change state before answering, up to 20. | [optional] 

### Return type

[**ObservatoryV1GetAuditQueryResponse**](ObservatoryV1GetAuditQueryResponse.md)

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

# **get_audit_query_results**
> ObservatoryV1GetAuditQueryResultsResponse get_audit_query_results(cluster_id, query_id, page_size=page_size, page_token=page_token)

Read audit log query results

Pages through the events of a query that has succeeded. Results stay readable for 24 hours.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.observatory_v1_get_audit_query_results_response import ObservatoryV1GetAuditQueryResultsResponse
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
    api_instance = vpcloud_client.KubernetesAuditApi(api_client)
    cluster_id = 'cluster_id_example' # str | A cluster your organization owns.
    query_id = 'query_id_example' # str | The queryId that createAuditQuery returned.
    page_size = 56 # int | Events per page, up to 1000. Defaults to 500. (optional)
    page_token = 'page_token_example' # str | The nextPageToken of the previous page. Omit it for the first page. (optional)

    try:
        # Read audit log query results
        api_response = api_instance.get_audit_query_results(cluster_id, query_id, page_size=page_size, page_token=page_token)
        print("The response of KubernetesAuditApi->get_audit_query_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesAuditApi->get_audit_query_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cluster_id** | **str**| A cluster your organization owns. | 
 **query_id** | **str**| The queryId that createAuditQuery returned. | 
 **page_size** | **int**| Events per page, up to 1000. Defaults to 500. | [optional] 
 **page_token** | **str**| The nextPageToken of the previous page. Omit it for the first page. | [optional] 

### Return type

[**ObservatoryV1GetAuditQueryResultsResponse**](ObservatoryV1GetAuditQueryResultsResponse.md)

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

