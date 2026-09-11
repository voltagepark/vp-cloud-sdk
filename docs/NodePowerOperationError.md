# NodePowerOperationError

Error details on FAILURE or TIMED_OUT. Null on success or non-terminal.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Machine-readable error code. | 
**message** | **str** | Human-readable error description. | 
**reset_issued** | **str** | Whether the reset command was actually sent to the hardware. | 

## Example

```python
from vpcloud_client.models.node_power_operation_error import NodePowerOperationError

# TODO update the JSON string below
json = "{}"
# create an instance of NodePowerOperationError from a JSON string
node_power_operation_error_instance = NodePowerOperationError.from_json(json)
# print the JSON string representation of the object
print(NodePowerOperationError.to_json())

# convert the object into a dict
node_power_operation_error_dict = node_power_operation_error_instance.to_dict()
# create an instance of NodePowerOperationError from a dict
node_power_operation_error_from_dict = NodePowerOperationError.from_dict(node_power_operation_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


