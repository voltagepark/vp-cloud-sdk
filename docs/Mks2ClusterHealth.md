# Mks2ClusterHealth

Comprehensive managed Kubernetes cluster health snapshot. Mirrors the Kubernetes API; `status` is the only required field (upstream always emits an overall health), every other field is optional and may be absent depending on which monitors have run. Consumers should treat missing fields as 'no signal' rather than 'healthy'.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**Mks2HealthStatus**](Mks2HealthStatus.md) |  | 
**control_plane** | [**Mks2ControlPlaneHealth**](Mks2ControlPlaneHealth.md) |  | [optional] 
**nodes** | [**List[Mks2NodeHealth]**](Mks2NodeHealth.md) | Per-worker-node health entries. Always worker-side; control-plane health lives in the controlPlane field above. | [optional] 
**network** | [**Mks2NetworkHealth**](Mks2NetworkHealth.md) |  | [optional] 
**addons** | [**Mks2AddonsHealth**](Mks2AddonsHealth.md) |  | [optional] 
**last_updated** | **datetime** | When the upstream health-collector last produced this snapshot. Absent if the collector has not run yet. | [optional] 
**last_healthy_at** | **datetime** | Last time the cluster overall reported healthy. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_cluster_health import Mks2ClusterHealth

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2ClusterHealth from a JSON string
mks2_cluster_health_instance = Mks2ClusterHealth.from_json(json)
# print the JSON string representation of the object
print(Mks2ClusterHealth.to_json())

# convert the object into a dict
mks2_cluster_health_dict = mks2_cluster_health_instance.to_dict()
# create an instance of Mks2ClusterHealth from a dict
mks2_cluster_health_from_dict = Mks2ClusterHealth.from_dict(mks2_cluster_health_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


