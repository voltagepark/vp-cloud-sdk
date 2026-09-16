# vpcloud_client.StorageApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_storage_view**](StorageApi.md#get_storage_view) | **GET** /v1/fleets/{fleetId}/storage/views/{view} | Get a VAST storage view
[**list_storage_views**](StorageApi.md#list_storage_views) | **GET** /v1/fleets/{fleetId}/storage/views | List VAST storage views


# **get_storage_view**
> StorageView get_storage_view(fleet_id, view)

Get a VAST storage view

Returns a single physical VAST storage view by mount point. Org-scoped: the caller's JWT org must own the fleet. The `state` field on the response is the source of truth for provisioning progress; poll this endpoint after a 202 from add/update until `state == "active"` (or `unhealthy` to fail fast).

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.storage_view import StorageView
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
    api_instance = vpcloud_client.StorageApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    view = 'view_example' # str | Storage view identifier (mount point, without a leading slash).

    try:
        # Get a VAST storage view
        api_response = api_instance.get_storage_view(fleet_id, view)
        print("The response of StorageApi->get_storage_view:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StorageApi->get_storage_view: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **view** | **str**| Storage view identifier (mount point, without a leading slash). | 

### Return type

[**StorageView**](StorageView.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The storage view. |  -  |
**400** | Malformed reservation identifier or invalid view path segment |  -  |
**401** | Missing or invalid JWT |  -  |
**404** | Fleet not found (or not owned by the caller&#39;s org), or storage view not found |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream infrastructure service returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_storage_views**
> StorageViewListResponse list_storage_views(fleet_id)

List VAST storage views

Lists the physical VAST storage views (mount points and their quotas) provisioned for the fleet's reservation. Org-scoped: the caller's JWT org must own the fleet. Each returned view carries a `state` field; use it to confirm provisioning completion (poll until `state == "active"`). If the fleet exists but storage has not been materialized yet, returns 200 with `items: []` and `storagePending: true`.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.storage_view_list_response import StorageViewListResponse
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
    api_instance = vpcloud_client.StorageApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier

    try:
        # List VAST storage views
        api_response = api_instance.list_storage_views(fleet_id)
        print("The response of StorageApi->list_storage_views:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StorageApi->list_storage_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

[**StorageViewListResponse**](StorageViewListResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Storage views for the fleet&#39;s reservation. When the fleet exists but storage has not been materialized yet, &#x60;items&#x60; is empty and &#x60;storagePending&#x60; is true. |  -  |
**400** | Fleet&#39;s stored reservation identifier is malformed |  -  |
**401** | Missing or invalid JWT |  -  |
**404** | Fleet not found (or not owned by the caller&#39;s org) |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream infrastructure service returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

