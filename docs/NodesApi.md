# vpcloud_client.NodesApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_node_by_fleet_id**](NodesApi.md#get_node_by_fleet_id) | **GET** /v1/fleets/{fleetId}/nodes/{nodeId} | Get node details
[**list_nodes_by_fleet_id**](NodesApi.md#list_nodes_by_fleet_id) | **GET** /v1/fleets/{fleetId}/nodes | List nodes in a fleet


# **get_node_by_fleet_id**
> Node get_node_by_fleet_id(fleet_id, node_id)

Get node details

Get detailed information about a specific GPU node, including IP addresses, health status, and connection details.

**When to use:**
- Get SSH connection info for a specific node
- Check detailed health status of a node
- Troubleshoot issues with a particular node
- Display node details in your UI

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.node import Node
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
    api_instance = vpcloud_client.NodesApi(api_client)
    fleet_id = '900e8eac-2b1f-421f-a635-72556268b41f' # str | Fleet identifier
    node_id = 'i-0abc123def456' # str | Node identifier (from list nodes response)

    try:
        # Get node details
        api_response = api_instance.get_node_by_fleet_id(fleet_id, node_id)
        print("The response of NodesApi->get_node_by_fleet_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NodesApi->get_node_by_fleet_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| Node identifier (from list nodes response) | 

### Return type

[**Node**](Node.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns complete node information |  -  |
**404** | Node not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_nodes_by_fleet_id**
> ListNodesResponse list_nodes_by_fleet_id(fleet_id, limit=limit, next_token=next_token)

List nodes in a fleet

Get all GPU nodes in a fleet with their current status, IP addresses, and health information.

**When to use:**
- Display node list in your fleet dashboard
- Check which nodes are ready for workloads
- Monitor node health across the fleet
- Get SSH connection details for nodes

**Response includes:** Node status, private/public IPs, GPU info, and health status.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.list_nodes_response import ListNodesResponse
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
    api_instance = vpcloud_client.NodesApi(api_client)
    fleet_id = '900e8eac-2b1f-421f-a635-72556268b41f' # str | Fleet identifier
    limit = 100 # int | Nodes per page (default: 100) (optional) (default to 100)
    next_token = 'next_token_example' # str | Token from previous response for next page (optional)

    try:
        # List nodes in a fleet
        api_response = api_instance.list_nodes_by_fleet_id(fleet_id, limit=limit, next_token=next_token)
        print("The response of NodesApi->list_nodes_by_fleet_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NodesApi->list_nodes_by_fleet_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **limit** | **int**| Nodes per page (default: 100) | [optional] [default to 100]
 **next_token** | **str**| Token from previous response for next page | [optional] 

### Return type

[**ListNodesResponse**](ListNodesResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns paginated list of nodes |  -  |
**400** | Bad request - invalid pagination parameters |  -  |
**404** | Fleet not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

