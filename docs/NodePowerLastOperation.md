# NodePowerLastOperation

Most recent power operation for the node.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | Operation identifier. | 
**reset_type** | **str** | Reset type requested. | 
**status** | **str** | Current operation status. ACCEPTED &#x3D; request received, execution not started. IN_PROGRESS &#x3D; execution underway, result not yet known. | 
**queued_at** | **int** | Unix millis when the operation was queued. | 
**completed_at** | **int** | Unix millis when the operation completed. Null if non-terminal. | [optional] 
**verified_power_state** | **str** | Power state verified on SUCCESS. Null otherwise. | [optional] 
**error** | [**NodePowerOperationError**](NodePowerOperationError.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.node_power_last_operation import NodePowerLastOperation

# TODO update the JSON string below
json = "{}"
# create an instance of NodePowerLastOperation from a JSON string
node_power_last_operation_instance = NodePowerLastOperation.from_json(json)
# print the JSON string representation of the object
print(NodePowerLastOperation.to_json())

# convert the object into a dict
node_power_last_operation_dict = node_power_last_operation_instance.to_dict()
# create an instance of NodePowerLastOperation from a dict
node_power_last_operation_from_dict = NodePowerLastOperation.from_dict(node_power_last_operation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


