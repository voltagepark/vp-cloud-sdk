# Mks2WorkerNodeDetail

Full MKS-2 worker-node detail: a superset of the list summary (Mks2WorkerNode) that adds per-node conditions, GPU info, labels/annotations, registration timestamps, and a live drain observation. Unlike the list (which only includes joined nodes), the per-node detail endpoint also resolves nodes that are registered but not yet joined. `gpuValidated` is a convenience mirror of `gpu.validated`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | MKS-2 worker-node identifier (registry id). Stable for the lifetime of the registry entry. | 
**name** | **str** | Kubernetes node name. Absent until the node has joined the cluster. | [optional] 
**registration_status** | [**Mks2WorkerNodeRegistrationStatus**](Mks2WorkerNodeRegistrationStatus.md) |  | 
**kubernetes_status** | [**Mks2WorkerNodeKubernetesStatus**](Mks2WorkerNodeKubernetesStatus.md) |  | [optional] 
**schedulable** | **bool** | Whether pods can be scheduled on this node (i.e. uncordoned). Absent when the node has not joined yet. | [optional] 
**drained** | **bool** | Live Kubernetes control-plane observation of whether workloads have drained from this node. True when every Pod currently bound to the node is terminal, a mirror Pod, or owned by a live DaemonSet. False when any other Pod remains. Omitted before the node joins or when the tenant cluster cannot be fully observed. This field is independent from &#x60;schedulable&#x60;; callers preparing maintenance must also verify the node is cordoned. The observation is point-in-time and does not prove that no out-of-band process is running on the host. | [optional] [readonly] 
**gpu_validated** | **bool** | Whether MKS-2 has run GPU validation against this node and it passed. Convenience mirror of gpu.validated; absent when no GPU info is available. | [optional] 
**conditions** | [**List[Mks2NodeCondition]**](Mks2NodeCondition.md) | Node conditions passed through from the tenant Kubernetes node, including custom MKS conditions. Absent until the node has joined. | [optional] 
**gpu** | [**Mks2GpuInfo**](Mks2GpuInfo.md) |  | [optional] 
**registered_at** | **datetime** | When the node was added to the MKS-2 worker registry. | [optional] 
**joined_at** | **datetime** | When the node joined the Kubernetes cluster. Null/absent for registered-but-not-yet-joined nodes. | [optional] 
**labels** | **Dict[str, str]** | Kubernetes node labels. Absent until the node has joined. | [optional] 
**annotations** | **Dict[str, str]** | Kubernetes node annotations. Absent until the node has joined. | [optional] 
**public_ip** | **str** | Public IPv4 address of the node, used for source-IP-based request routing. Absent when the node was registered without a public IP. | [optional] 
**taints** | [**List[Mks2NodeTaint]**](Mks2NodeTaint.md) | Live Kubernetes node taints. Absent until the node has joined. The admin/CX node-details policy uses the maintenance taint for powerActionReadiness. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_worker_node_detail import Mks2WorkerNodeDetail

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2WorkerNodeDetail from a JSON string
mks2_worker_node_detail_instance = Mks2WorkerNodeDetail.from_json(json)
# print the JSON string representation of the object
print(Mks2WorkerNodeDetail.to_json())

# convert the object into a dict
mks2_worker_node_detail_dict = mks2_worker_node_detail_instance.to_dict()
# create an instance of Mks2WorkerNodeDetail from a dict
mks2_worker_node_detail_from_dict = Mks2WorkerNodeDetail.from_dict(mks2_worker_node_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


