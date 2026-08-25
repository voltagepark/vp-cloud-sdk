# NodePowerState

Live BMC power state for a node, read from Thundercat/Redfish on every call - not cached or stored by Harbor.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** | Node identifier. | 
**power_state** | **str** | Live power state as reported by the BMC. | 

## Example

```python
from vpcloud_client.models.node_power_state import NodePowerState

# TODO update the JSON string below
json = "{}"
# create an instance of NodePowerState from a JSON string
node_power_state_instance = NodePowerState.from_json(json)
# print the JSON string representation of the object
print(NodePowerState.to_json())

# convert the object into a dict
node_power_state_dict = node_power_state_instance.to_dict()
# create an instance of NodePowerState from a dict
node_power_state_from_dict = NodePowerState.from_dict(node_power_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


