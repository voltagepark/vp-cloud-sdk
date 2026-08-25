# NodePowerOperation

Requests a power transition on a node. Thundercat enforces which transitions are valid given the node's current power state (e.g. `On` is only valid when the node is off). Customers may only request `On` or `ForceRestart`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reset_type** | **str** | Redfish ComputerSystem.Reset type to apply via the node&#39;s BMC. | 

## Example

```python
from vpcloud_client.models.node_power_operation import NodePowerOperation

# TODO update the JSON string below
json = "{}"
# create an instance of NodePowerOperation from a JSON string
node_power_operation_instance = NodePowerOperation.from_json(json)
# print the JSON string representation of the object
print(NodePowerOperation.to_json())

# convert the object into a dict
node_power_operation_dict = node_power_operation_instance.to_dict()
# create an instance of NodePowerOperation from a dict
node_power_operation_from_dict = NodePowerOperation.from_dict(node_power_operation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


