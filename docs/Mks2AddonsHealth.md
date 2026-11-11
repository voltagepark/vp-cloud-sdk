# Mks2AddonsHealth

Per-addon health monitors. Each sub-field is absent until its monitor is wired upstream; treat absence as no signal, not as healthy.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**slurm** | [**Mks2ComponentHealth**](Mks2ComponentHealth.md) |  | [optional] 
**prometheus** | [**Mks2ComponentHealth**](Mks2ComponentHealth.md) |  | [optional] 
**efs** | [**Mks2ComponentHealth**](Mks2ComponentHealth.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.mks2_addons_health import Mks2AddonsHealth

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2AddonsHealth from a JSON string
mks2_addons_health_instance = Mks2AddonsHealth.from_json(json)
# print the JSON string representation of the object
print(Mks2AddonsHealth.to_json())

# convert the object into a dict
mks2_addons_health_dict = mks2_addons_health_instance.to_dict()
# create an instance of Mks2AddonsHealth from a dict
mks2_addons_health_from_dict = Mks2AddonsHealth.from_dict(mks2_addons_health_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


