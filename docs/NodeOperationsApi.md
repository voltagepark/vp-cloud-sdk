# vpcloud_client.NodeOperationsApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_node_power_operation**](NodeOperationsApi.md#create_node_power_operation) | **POST** /v1/fleets/{fleetId}/nodes/{nodeId}/power | Queue a node power operation


# **create_node_power_operation**
> NodePowerOperationQueued create_node_power_operation(fleet_id, node_id, idempotency_key, node_power_operation)

Queue a node power operation

Queues a power transition on a node via its BMC. Valid transitions depend on the node's current power state. All reset types require both `cust:fleets:nodes:power` (route gate) and `cust:fleets:nodes:power-off` (handler gate, cust-admin). Requests missing the `power-off` permission are rejected with 403. Unknown reset types are rejected with 400.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.node_power_operation import NodePowerOperation
from vpcloud_client.models.node_power_operation_queued import NodePowerOperationQueued
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
    api_instance = vpcloud_client.NodeOperationsApi(api_client)
    fleet_id = '900e8eac-2b1f-421f-a635-72556268b41f' # str | Fleet identifier
    node_id = 'g311' # str | Node identifier (from list nodes response)
    idempotency_key = 'idempotency_key_example' # str | Unique key for idempotent retries. Required for power operations.
    node_power_operation = vpcloud_client.NodePowerOperation() # NodePowerOperation | 

    try:
        # Queue a node power operation
        api_response = api_instance.create_node_power_operation(fleet_id, node_id, idempotency_key, node_power_operation)
        print("The response of NodeOperationsApi->create_node_power_operation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NodeOperationsApi->create_node_power_operation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| Node identifier (from list nodes response) | 
 **idempotency_key** | **str**| Unique key for idempotent retries. Required for power operations. | 
 **node_power_operation** | [**NodePowerOperation**](NodePowerOperation.md)|  | 

### Return type

[**NodePowerOperationQueued**](NodePowerOperationQueued.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Idempotent replay — the operation already completed. The response body contains the terminal outcome. |  -  |
**202** | Power operation accepted and queued. |  -  |
**400** | Invalid request body or unknown resetType |  -  |
**403** | Authenticated but missing the required cust:fleets:nodes:power-off permission |  -  |
**404** | Fleet or node not found, or the fleet has no reservation yet |  -  |
**409** | Requested transition conflicts with the node&#39;s current power state, or a request with the same Idempotency-Key is currently in progress |  -  |
**422** | Idempotency-Key reused with a different request body |  -  |
**423** | Another power operation is already in progress on this node |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream infrastructure service returned an error, or the node&#39;s BMC is unreachable |  -  |
**503** | Born-dead — the operation was recorded but the upstream BMC queue rejected it immediately. The response body contains the failure record. Clients may retry with a new Idempotency-Key. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

