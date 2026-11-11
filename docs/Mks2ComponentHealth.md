# Mks2ComponentHealth

Health for a single named component (e.g. Cilium, konnectivity, an addon). Every field is optional. `reason` is human-readable diagnostic text - do not match programmatically. `lastHealthyAt` is the last time the component reported healthy; `lastUpdated` is when the most recent observation was made (regardless of whether it was healthy).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**Mks2HealthStatus**](Mks2HealthStatus.md) |  | [optional] 
**reason** | **str** | Human-readable status detail; not stable for programmatic matching. | [optional] 
**last_updated** | **datetime** | When this component&#39;s status was last observed. | [optional] 
**last_healthy_at** | **datetime** | Last timestamp at which this component reported healthy. Absent if upstream did not include it. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_component_health import Mks2ComponentHealth

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2ComponentHealth from a JSON string
mks2_component_health_instance = Mks2ComponentHealth.from_json(json)
# print the JSON string representation of the object
print(Mks2ComponentHealth.to_json())

# convert the object into a dict
mks2_component_health_dict = mks2_component_health_instance.to_dict()
# create an instance of Mks2ComponentHealth from a dict
mks2_component_health_from_dict = Mks2ComponentHealth.from_dict(mks2_component_health_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


