# NodePowerOperationQueued

Confirmation that a power operation was accepted and queued. The operation is asynchronous - use `operationId` to track operation status via GET.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** | Node identifier. | 
**reset_type** | **str** | Power action that was queued. One of &#x60;On&#x60;, &#x60;ForceOff&#x60;, &#x60;GracefulShutdown&#x60;, or &#x60;ForceRestart&#x60;. | 
**power_state_before** | **str** | Live BMC power state read immediately before queueing the operation. | 
**status** | **str** | Queue status for the requested operation. | 
**operation_id** | **str** | Unique identifier for the power operation. Use this to track operation status via GET. | 

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


