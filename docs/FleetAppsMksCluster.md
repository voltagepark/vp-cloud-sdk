# FleetAppsMksCluster

MK8s (managed Kubernetes) cluster information for this fleet

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cluster_id** | **str** | MK8s cluster ID | 
**cluster_name** | **str** | MK8s cluster name | 
**kubernetes_version** | **str** | Kubernetes version running on the cluster | [optional] 
**installation_status** | **str** | MK8s installation status on the fleet | 
**cluster_status** | **str** | Current MK8s cluster status from MKS API | [optional] 
**kubeconfig** | **str** | The kubeconfig for accessing the cluster (if available) | [optional] 
**auth_config_b64** | **str** | Base64-encoded authentication configuration for the cluster | [optional] 
**service_links** | [**KubernetesServiceLinks**](KubernetesServiceLinks.md) |  | [optional] 
**control_plane_node_count** | **int** | Number of control plane nodes | [optional] 
**ready_control_plane_node_count** | **int** | Number of ready control plane nodes | [optional] 
**worker_node_count** | **int** | Number of worker nodes | [optional] 
**ready_worker_node_count** | **int** | Number of ready worker nodes | [optional] 
**addons** | **List[str]** | List of installed addons | [optional] 
**created_at** | **str** | Timestamp when the cluster was created | [optional] 

## Example

```python
from vpcloud_client.models.fleet_apps_mks_cluster import FleetAppsMksCluster

# TODO update the JSON string below
json = "{}"
# create an instance of FleetAppsMksCluster from a JSON string
fleet_apps_mks_cluster_instance = FleetAppsMksCluster.from_json(json)
# print the JSON string representation of the object
print(FleetAppsMksCluster.to_json())

# convert the object into a dict
fleet_apps_mks_cluster_dict = fleet_apps_mks_cluster_instance.to_dict()
# create an instance of FleetAppsMksCluster from a dict
fleet_apps_mks_cluster_from_dict = FleetAppsMksCluster.from_dict(fleet_apps_mks_cluster_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


