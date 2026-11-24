# vpcloud_client.FleetOperationsApi

All URIs are relative to *https://api.sea1.voltagepark.com*, the default `Configuration.host`. Set `host` to the regional API endpoint for your fleets' region.

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
import os
import vpcloud_client
from vpcloud_client.models.modify_storage_request import ModifyStorageRequest
from vpcloud_client.models.modify_storage_response import ModifyStorageResponse
from vpcloud_client.rest import ApiException
from pprint import pprint

# Set host to the regional API endpoint for your fleets' region, for example
# https://api.iad1.voltagepark.com. It defaults to https://api.sea1.voltagepark.com.
# The SDK exchanges your application's client credentials for an access token.
# See configuration.py for a list of all supported configuration parameters.
configuration = vpcloud_client.Configuration(
    host = "https://api.sea1.voltagepark.com",
    client_id = os.environ["VPCLOUD_CLIENT_ID"],
    client_secret = os.environ["VPCLOUD_CLIENT_SECRET"],
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

