# Mks2ControlPlaneHealth

Health of the cluster's control plane (managed Kubernetes tenant-cluster API server + controller-manager + scheduler). Replicas and readyReplicas reflect the live observed counts when published, falling back to the desired count from the spec when no observed status is available yet.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**Mks2HealthStatus**](Mks2HealthStatus.md) |  | [optional] 
**replicas** | **int** | Total control-plane replicas (observed if available, else desired). | [optional] 
**ready_replicas** | **int** | Number of control-plane replicas currently Ready. | [optional] 
**reason** | **str** | Human-readable detail; populated when degraded/unhealthy. | [optional] 
**last_updated** | **datetime** | When the control plane&#39;s status was last observed. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_control_plane_health import Mks2ControlPlaneHealth

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2ControlPlaneHealth from a JSON string
mks2_control_plane_health_instance = Mks2ControlPlaneHealth.from_json(json)
# print the JSON string representation of the object
print(Mks2ControlPlaneHealth.to_json())

# convert the object into a dict
mks2_control_plane_health_dict = mks2_control_plane_health_instance.to_dict()
# create an instance of Mks2ControlPlaneHealth from a dict
mks2_control_plane_health_from_dict = Mks2ControlPlaneHealth.from_dict(mks2_control_plane_health_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


