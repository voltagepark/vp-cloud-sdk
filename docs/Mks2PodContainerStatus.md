# Mks2PodContainerStatus

Status of a single container in an MKS-2 pod.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Container name. | [optional] 
**ready** | **bool** | Whether the container passed its readiness probe. | [optional] 
**restart_count** | **int** | Number of times the container has restarted. | [optional] 
**state** | [**Mks2PodContainerState**](Mks2PodContainerState.md) | Current container state. | [optional] 
**reason** | **str** | Machine-readable reason for the current state (set when waiting/terminated). | [optional] 
**message** | **str** | Human-readable message describing the current state. | [optional] 
**started_at** | **datetime** | When the container last started running, when reported. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_pod_container_status import Mks2PodContainerStatus

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2PodContainerStatus from a JSON string
mks2_pod_container_status_instance = Mks2PodContainerStatus.from_json(json)
# print the JSON string representation of the object
print(Mks2PodContainerStatus.to_json())

# convert the object into a dict
mks2_pod_container_status_dict = mks2_pod_container_status_instance.to_dict()
# create an instance of Mks2PodContainerStatus from a dict
mks2_pod_container_status_from_dict = Mks2PodContainerStatus.from_dict(mks2_pod_container_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


