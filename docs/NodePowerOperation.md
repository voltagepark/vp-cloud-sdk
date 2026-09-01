# NodePowerOperation

Requests a power transition on a node. Valid transitions depend on the node's current power state (e.g. `On` is only valid when the node is off). `On` and `ForceRestart` require `cust:fleets:nodes:power`. `ForceOff` and `GracefulShutdown` also require `cust:fleets:nodes:power-off`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reset_type** | **str** | Power action to apply. &#x60;On&#x60; powers the node on. &#x60;ForceOff&#x60; cuts power immediately and leaves the node off. &#x60;GracefulShutdown&#x60; requests an OS shutdown and leaves the node off. &#x60;ForceRestart&#x60; reboots immediately. | 

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


