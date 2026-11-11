# vpcloud_client.FleetsApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_fleet**](FleetsApi.md#get_fleet) | **GET** /v1/fleets/{fleetId} | Get fleet details
[**get_fleet_health**](FleetsApi.md#get_fleet_health) | **GET** /v1/fleets/{fleetId}/health | Get fleet health metrics
[**get_fleet_history**](FleetsApi.md#get_fleet_history) | **GET** /v1/fleets/{fleetId}/history | Get fleet event history
[**list_fleets**](FleetsApi.md#list_fleets) | **GET** /v1/fleets | List your fleets


# **get_fleet**
> Fleet get_fleet(fleet_id)

Get fleet details

Get complete information about a specific fleet, including configuration, status, and current node count.

**When to use:**
- Display fleet details in your application
- Check current fleet configuration before scaling
- Monitor fleet status and health

**Response includes:** GPU type, node count, region, networking, storage, and current operational status.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.fleet import Fleet
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
    api_instance = vpcloud_client.FleetsApi(api_client)
    fleet_id = '900e8eac-2b1f-421f-a635-72556268b41f' # str | Fleet identifier

    try:
        # Get fleet details
        api_response = api_instance.get_fleet(fleet_id)
        print("The response of FleetsApi->get_fleet:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetsApi->get_fleet: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

[**Fleet**](Fleet.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns complete fleet information |  -  |
**404** | Fleet not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fleet_health**
> FleetHealthResponse get_fleet_health(fleet_id)

Get fleet health metrics

Get detailed health information about fleet nodes, including connectivity and operational status. Only available for ACTIVE fleets with nodes.

**When to use:**
- Check if nodes are healthy before running workloads
- Diagnose connectivity or performance issues
- Monitor fleet operational health

**Note:** Returns 422 if fleet is not active or has no nodes yet.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.fleet_health_response import FleetHealthResponse
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
    api_instance = vpcloud_client.FleetsApi(api_client)
    fleet_id = '900e8eac-2b1f-421f-a635-72556268b41f' # str | Fleet identifier

    try:
        # Get fleet health metrics
        api_response = api_instance.get_fleet_health(fleet_id)
        print("The response of FleetsApi->get_fleet_health:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetsApi->get_fleet_health: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

[**FleetHealthResponse**](FleetHealthResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns health metrics for all nodes in the fleet |  -  |
**404** | Fleet not found |  -  |
**422** | Fleet is not in ACTIVE status or has inconsistent state (ACTIVE fleet with no nodes) |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fleet_history**
> FleetHistoryResponse get_fleet_history(fleet_id, limit=limit, next_token=next_token)

Get fleet event history

Get the lifecycle history for a fleet, newest first: creation, status changes (including scaling and termination), storage changes, and node remediation requests.

**When to use:**
- Show fleet activity timeline in your UI
- Audit what happened to a fleet
- Debug issues by reviewing recent events

**Pagination:** Some events are omitted from the history, so a page can contain fewer events than `limit`, or none, while `nextToken` is still returned. Keep requesting pages until `nextToken` is absent.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.fleet_history_response import FleetHistoryResponse
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
    api_instance = vpcloud_client.FleetsApi(api_client)
    fleet_id = '900e8eac-2b1f-421f-a635-72556268b41f' # str | Fleet identifier
    limit = 1000 # int | Maximum number of events per page (default: 1000, max: 1000) (optional) (default to 1000)
    next_token = 'next_token_example' # str | Token from previous response to get next page of events (optional)

    try:
        # Get fleet event history
        api_response = api_instance.get_fleet_history(fleet_id, limit=limit, next_token=next_token)
        print("The response of FleetsApi->get_fleet_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetsApi->get_fleet_history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **limit** | **int**| Maximum number of events per page (default: 1000, max: 1000) | [optional] [default to 1000]
 **next_token** | **str**| Token from previous response to get next page of events | [optional] 

### Return type

[**FleetHistoryResponse**](FleetHistoryResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns paginated fleet history events |  -  |
**404** | Fleet not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_fleets**
> ListFleetsResponse list_fleets(limit=limit, next_token=next_token)

List your fleets

Get all GPU fleets in your organization. Each fleet represents a cluster of GPU nodes ready for your workloads.

**When to use:**
- Display fleets in your dashboard
- Check which fleets are currently active
- Get an overview of your GPU infrastructure

**Response Format:** Always returns ListFleetsResponse with `fleets` array, `limit`, and `nextToken` fields.

**Pagination:** Optional - add `limit` parameter to paginate. Without `limit`, returns all fleets with `limit: null` and `nextToken: null`.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.list_fleets_response import ListFleetsResponse
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
    api_instance = vpcloud_client.FleetsApi(api_client)
    limit = 56 # int | Optional: Maximum number of fleets to return per page (0-100). Use 0 to get all results in paginated format. If provided, response includes pagination metadata. (optional)
    next_token = 'next_token_example' # str | Optional: Pagination token from previous response to retrieve the next page. Only valid when 'limit' is provided. (optional)

    try:
        # List your fleets
        api_response = api_instance.list_fleets(limit=limit, next_token=next_token)
        print("The response of FleetsApi->list_fleets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetsApi->list_fleets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Optional: Maximum number of fleets to return per page (0-100). Use 0 to get all results in paginated format. If provided, response includes pagination metadata. | [optional] 
 **next_token** | **str**| Optional: Pagination token from previous response to retrieve the next page. Only valid when &#39;limit&#39; is provided. | [optional] 

### Return type

[**ListFleetsResponse**](ListFleetsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of fleets retrieved successfully. Always returns ListFleetsResponse with unified format. When pagination not used, limit and nextToken are null. |  -  |
**400** | Bad request - invalid pagination parameters |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

