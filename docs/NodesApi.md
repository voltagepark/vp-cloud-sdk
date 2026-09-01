# vpcloud_client.NodesApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_fleet_node_details**](NodesApi.md#get_fleet_node_details) | **GET** /v1/fleets/{fleetId}/nodes/{nodeId}/details | Get consolidated node details
[**get_node_by_fleet_id**](NodesApi.md#get_node_by_fleet_id) | **GET** /v1/fleets/{fleetId}/nodes/{nodeId} | Get node details
[**get_node_power_state**](NodesApi.md#get_node_power_state) | **GET** /v1/fleets/{fleetId}/nodes/{nodeId}/power | Get node power state
[**list_nodes_by_fleet_id**](NodesApi.md#list_nodes_by_fleet_id) | **GET** /v1/fleets/{fleetId}/nodes | List nodes in a fleet


# **get_fleet_node_details**
> NodeDetails get_fleet_node_details(fleet_id, node_id)

Get consolidated node details

Returns consolidated single-node details for the node-details page: base physical fields (publicIp only), advisory powerActionReadiness, and optional managed-service data. privateIp and topology are admin-only (see AdminNodeDetails). Org-scoped: the caller's JWT org must own the fleet and the node must belong to that fleet.

Net-new endpoint — does not replace GET /v1/fleets/{fleetId}/nodes/{nodeId}.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.node_details import NodeDetails
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
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    node_id = 'g0546' # str | Node identifier (ThunderCat node name / fleet node id)

    try:
        # Get consolidated node details
        api_response = api_instance.get_fleet_node_details(fleet_id, node_id)
        print("The response of NodesApi->get_fleet_node_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NodesApi->get_fleet_node_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| Node identifier (ThunderCat node name / fleet node id) | 

### Return type

[**NodeDetails**](NodeDetails.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns consolidated node details |  -  |
**401** | Authentication required |  -  |
**404** | Fleet or node not found, or node not in the caller&#39;s org/fleet |  -  |
**500** | Internal server error |  -  |
**502** | Upstream ThunderCat failure |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

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

# **get_node_power_state**
> NodePowerState get_node_power_state(fleet_id, node_id)

Get node power state

Read the node's live BMC power state via Redfish. Not cached or stored by Harbor - every call reads the BMC directly.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.node_power_state import NodePowerState
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
    node_id = 'g311' # str | Node identifier (from list nodes response)

    try:
        # Get node power state
        api_response = api_instance.get_node_power_state(fleet_id, node_id)
        print("The response of NodesApi->get_node_power_state:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NodesApi->get_node_power_state: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| Node identifier (from list nodes response) | 

### Return type

[**NodePowerState**](NodePowerState.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The node&#39;s live power state. |  -  |
**400** | Fleet has an invalid Thundercat reservation ID, or nodeId is invalid |  -  |
**404** | Fleet or node not found, or the fleet has no Thundercat reservation yet |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream Thundercat returned an error, or the node&#39;s BMC is unreachable |  -  |

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

