# Mks2NodeCondition

A single condition on an MKS-2 worker node. Reported from the node's Kubernetes status; includes standard Kubernetes node conditions (Ready, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable) and additional GPU/health conditions (e.g. GPUValidated).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Condition type (e.g. Ready, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable, GPUValidated). | [optional] 
**status** | **str** | Condition status. One of True, False, Unknown. | [optional] 
**reason** | **str** | Machine-readable reason for the condition&#39;s last transition. | [optional] 
**message** | **str** | Human-readable message describing the condition. | [optional] 
**last_transition_time** | **datetime** | When the condition last transitioned. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_node_condition import Mks2NodeCondition

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2NodeCondition from a JSON string
mks2_node_condition_instance = Mks2NodeCondition.from_json(json)
# print the JSON string representation of the object
print(Mks2NodeCondition.to_json())

# convert the object into a dict
mks2_node_condition_dict = mks2_node_condition_instance.to_dict()
# create an instance of Mks2NodeCondition from a dict
mks2_node_condition_from_dict = Mks2NodeCondition.from_dict(mks2_node_condition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


