# NodePowerOperationQueued

Confirmation that a power operation was accepted and queued. The operation is asynchronous - use `taskId` to correlate with logs, and re-`GET` the node's power state to observe the outcome.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** | Node identifier. | 
**reset_type** | **str** | The queued Redfish ComputerSystem.Reset type. | 
**power_state_before** | **str** | Live BMC power state read immediately before queueing the operation. | 
**status** | **str** | Queue status for the requested operation. | 
**task_id** | **str** | Identifier for the queued power operation, for log correlation. | 

## Example

```python
from vpcloud_client.models.node_power_operation_queued import NodePowerOperationQueued

# TODO update the JSON string below
json = "{}"
# create an instance of NodePowerOperationQueued from a JSON string
node_power_operation_queued_instance = NodePowerOperationQueued.from_json(json)
# print the JSON string representation of the object
print(NodePowerOperationQueued.to_json())

# convert the object into a dict
node_power_operation_queued_dict = node_power_operation_queued_instance.to_dict()
# create an instance of NodePowerOperationQueued from a dict
node_power_operation_queued_from_dict = NodePowerOperationQueued.from_dict(node_power_operation_queued_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


