# Mks2PodCondition

A single condition on an MKS-2 pod, reported from the pod's Kubernetes status.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Condition type (e.g. PodScheduled, Initialized, ContainersReady, Ready, PodReadyToStartContainers). | [optional] 
**status** | [**Mks2PodConditionStatus**](Mks2PodConditionStatus.md) | Condition status. | [optional] 
**reason** | **str** | Machine-readable reason for the condition&#39;s last transition. | [optional] 
**message** | **str** | Human-readable message describing the condition. | [optional] 
**last_transition_time** | **datetime** | When the condition last transitioned. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_pod_condition import Mks2PodCondition

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2PodCondition from a JSON string
mks2_pod_condition_instance = Mks2PodCondition.from_json(json)
# print the JSON string representation of the object
print(Mks2PodCondition.to_json())

# convert the object into a dict
mks2_pod_condition_dict = mks2_pod_condition_instance.to_dict()
# create an instance of Mks2PodCondition from a dict
mks2_pod_condition_from_dict = Mks2PodCondition.from_dict(mks2_pod_condition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


