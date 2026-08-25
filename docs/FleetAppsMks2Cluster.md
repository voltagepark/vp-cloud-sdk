# FleetAppsMks2Cluster

MKS-2 (Kamaji-based managed Kubernetes) cluster information for this fleet. Distinct from FleetAppsMksCluster (legacy MKS-1) so the two contracts can evolve independently. Sensitive fields (kubeconfig) are intentionally not surfaced here; they are fetched via a separate endpoint.  Atomic populate-or-omit: when this object is present in a fleet response, every field is populated from a successful live MKS-2 GetCluster call. If MKS-2 is unreachable, this object is omitted from the parent FleetApps entirely - the response then has no mks2Cluster key at all. Clients should treat absent and present-but-incomplete as the same state (cluster details unavailable).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cluster_id** | **str** | MKS-2 cluster ID (sourced from DDB; stable across enrichment results) | 
**cluster_name** | **str** | MKS-2 cluster name as reported by MKS-2 | 
**kubernetes_version** | **str** | Kubernetes version running on the cluster (e.g. v1.35.0) | 
**cluster_status** | **str** | Live cluster status reported by MKS-2 (lowercase, mirrors mks2sdk.ClusterStatus). | 
**control_plane_replicas** | **int** | Desired number of control plane replicas | 
**control_plane_size** | **str** | Control plane resource tier, which determines the CPU and memory allocated to the Kubernetes API server. Omitted while the cluster&#39;s control plane is still being provisioned. | [optional] 
**datastore_type** | **str** | Whether the cluster runs on shared multi-tenant etcd or its own dedicated etcd cluster. Omitted when the cluster&#39;s etcd configuration is temporarily unavailable. | [optional] 
**nvidia_driver_version** | **str** | NVIDIA driver version installed via the GPU operator | 
**created_at** | **datetime** | Timestamp when the MKS-2 cluster was created | 
**node_counts** | [**FleetAppsMks2NodeCounts**](FleetAppsMks2NodeCounts.md) |  | 

## Example

```python
from vpcloud_client.models.fleet_apps_mks2_cluster import FleetAppsMks2Cluster

# TODO update the JSON string below
json = "{}"
# create an instance of FleetAppsMks2Cluster from a JSON string
fleet_apps_mks2_cluster_instance = FleetAppsMks2Cluster.from_json(json)
# print the JSON string representation of the object
print(FleetAppsMks2Cluster.to_json())

# convert the object into a dict
fleet_apps_mks2_cluster_dict = fleet_apps_mks2_cluster_instance.to_dict()
# create an instance of FleetAppsMks2Cluster from a dict
fleet_apps_mks2_cluster_from_dict = FleetAppsMks2Cluster.from_dict(fleet_apps_mks2_cluster_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


