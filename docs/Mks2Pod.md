# Mks2Pod

A pod in the fleet's MKS-2 cluster. `phase` is the raw Kubernetes pod phase; `status` is a derived human-readable status (e.g. Running, CrashLoopBackOff, Terminating).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Pod name. | 
**namespace** | **str** | Pod namespace. | 
**node_name** | **str** | Name of the node the pod is scheduled on. Absent for unscheduled pods. | [optional] 
**phase** | [**Mks2PodPhase**](Mks2PodPhase.md) | Raw Kubernetes pod phase. | [optional] 
**status** | **str** | Derived human-readable status (e.g. Running, CrashLoopBackOff, Init:0/1, Terminating). | [optional] 
**ip** | **str** | Pod IP address, when assigned. | [optional] 
**host_ip** | **str** | IP address of the host node, when assigned. | [optional] 
**restarts** | **int** | Total container restarts across the pod. | [optional] 
**created_at** | **datetime** | Pod creation timestamp. | [optional] 
**started_at** | **datetime** | When the pod started running, when reported. | [optional] 
**labels** | **Dict[str, str]** | Pod labels. | [optional] 
**conditions** | [**List[Mks2PodCondition]**](Mks2PodCondition.md) | Pod conditions reported by Kubernetes (e.g. PodScheduled, Initialized, ContainersReady, Ready). | [optional] 
**containers** | [**List[Mks2PodContainerStatus]**](Mks2PodContainerStatus.md) | Per-container statuses. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_pod import Mks2Pod

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2Pod from a JSON string
mks2_pod_instance = Mks2Pod.from_json(json)
# print the JSON string representation of the object
print(Mks2Pod.to_json())

# convert the object into a dict
mks2_pod_dict = mks2_pod_instance.to_dict()
# create an instance of Mks2Pod from a dict
mks2_pod_from_dict = Mks2Pod.from_dict(mks2_pod_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


