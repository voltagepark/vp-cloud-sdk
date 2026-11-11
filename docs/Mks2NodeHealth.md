# Mks2NodeHealth

Per-worker-node health snapshot. Identifier is the managed Kubernetes registry id; the upstream service intentionally does not expose Kubernetes node names or full conditions maps here - per-node detail belongs in the dedicated nodes endpoint.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Managed Kubernetes node identifier (registry ID). | [optional] 
**status** | [**Mks2HealthStatus**](Mks2HealthStatus.md) |  | [optional] 
**reason** | **str** | Human-readable detail; not stable for programmatic matching. | [optional] 
**last_updated** | **datetime** | When this node&#39;s health was last observed. | [optional] 
**last_healthy_at** | **datetime** | Last time this node reported healthy. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_node_health import Mks2NodeHealth

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2NodeHealth from a JSON string
mks2_node_health_instance = Mks2NodeHealth.from_json(json)
# print the JSON string representation of the object
print(Mks2NodeHealth.to_json())

# convert the object into a dict
mks2_node_health_dict = mks2_node_health_instance.to_dict()
# create an instance of Mks2NodeHealth from a dict
mks2_node_health_from_dict = Mks2NodeHealth.from_dict(mks2_node_health_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


