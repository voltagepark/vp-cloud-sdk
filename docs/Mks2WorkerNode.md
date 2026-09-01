# Mks2WorkerNode

Minimal MKS-2 worker-node info for list responses. The list payload is intentionally small; use the per-node detail endpoint (GET .../kubernetes-v2/nodes/{nodeId}) for the full node object with conditions, GPU info, and labels/annotations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | MKS-2 worker-node identifier (registry id). Stable for the lifetime of the registry entry. | 
**registration_status** | [**Mks2WorkerNodeRegistrationStatus**](Mks2WorkerNodeRegistrationStatus.md) |  | 
**kubernetes_status** | [**Mks2WorkerNodeKubernetesStatus**](Mks2WorkerNodeKubernetesStatus.md) |  | [optional] 
**schedulable** | **bool** | Whether pods can be scheduled on this node (i.e. uncordoned). Absent when the node has not joined yet. | [optional] 
**gpu_validated** | **bool** | Whether MKS-2 has run GPU validation against this node and it passed. Absent when no validation has run. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_worker_node import Mks2WorkerNode

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2WorkerNode from a JSON string
mks2_worker_node_instance = Mks2WorkerNode.from_json(json)
# print the JSON string representation of the object
print(Mks2WorkerNode.to_json())

# convert the object into a dict
mks2_worker_node_dict = mks2_worker_node_instance.to_dict()
# create an instance of Mks2WorkerNode from a dict
mks2_worker_node_from_dict = Mks2WorkerNode.from_dict(mks2_worker_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


