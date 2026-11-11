# vpcloud_client.FleetOperationsApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**modify_fleet_storage**](FleetOperationsApi.md#modify_fleet_storage) | **POST** /v1/fleets/{fleetId}/storage/modify | Resize fleet storage


# **modify_fleet_storage**
> ModifyStorageResponse modify_fleet_storage(fleet_id, modify_storage_request)

Resize fleet storage

Increase or decrease the storage capacity for your fleet. Only the size can be changed - mount points and number of storage volumes stay the same.

**When to use:**
- Increase storage when running out of space
- Decrease storage to reduce costs
- Adjust capacity for different workload requirements

**Important constraints:**
- Only change size - can't add/remove storage volumes
- Must match existing mount points exactly
- Fleet remains available during resize

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.modify_storage_request import ModifyStorageRequest
from vpcloud_client.models.modify_storage_response import ModifyStorageResponse
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
    api_instance = vpcloud_client.FleetOperationsApi(api_client)
    fleet_id = '900e8eac-2b1f-421f-a635-72556268b41f' # str | Fleet identifier
    modify_storage_request = vpcloud_client.ModifyStorageRequest() # ModifyStorageRequest | 

    try:
        # Resize fleet storage
        api_response = api_instance.modify_fleet_storage(fleet_id, modify_storage_request)
        print("The response of FleetOperationsApi->modify_fleet_storage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetOperationsApi->modify_fleet_storage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **modify_storage_request** | [**ModifyStorageRequest**](ModifyStorageRequest.md)|  | 

### Return type

[**ModifyStorageResponse**](ModifyStorageResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Storage modification initiated successfully |  -  |
**404** | Fleet not found |  -  |
**400** | Invalid storage modification request, or the storage service refused the change, for example because storage is not active. Retry later; contact support if it persists. |  -  |
**409** | The fleet does not have storage provisioned yet. |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

