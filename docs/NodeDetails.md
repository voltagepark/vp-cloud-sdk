# NodeDetails

Consolidated single-node details for the customer node-details page. Composes base physical-node fields (publicIp only — no privateIp / reservationId / nodeResourceName), advisory powerActionReadiness, and optional managedServices. Customer power readiness checks cluster join, cordon, and drain state. Topology, privateIp, reservationId, and nodeResourceName are admin-only (see AdminNodeDetails). Existing list/detail endpoints are unchanged.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_name** | **str** | Unique identifier for the node (ThunderCat Node.Name / MKS registry id). | 
**state** | [**NodeState**](NodeState.md) |  | 
**public_ip** | **str** | Public IP address of the node | 
**fleet_id** | **str** | Fleet ID associated with the node, if any | [optional] 
**power_action_readiness** | [**PowerActionReadiness**](PowerActionReadiness.md) |  | 
**managed_services** | [**NodeManagedServices**](NodeManagedServices.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.node_details import NodeDetails

# TODO update the JSON string below
json = "{}"
# create an instance of NodeDetails from a JSON string
node_details_instance = NodeDetails.from_json(json)
# print the JSON string representation of the object
print(NodeDetails.to_json())

# convert the object into a dict
node_details_dict = node_details_instance.to_dict()
# create an instance of NodeDetails from a dict
node_details_from_dict = NodeDetails.from_dict(node_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


