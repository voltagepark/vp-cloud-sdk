# Mks2NetworkHealth

Health of the cluster's networking layer. cilium covers the CNI; konnectivity covers API-server-to-worker connectivity. Both are absent until their respective monitors are wired upstream - treat absence as no signal, not as healthy.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cilium** | [**Mks2ComponentHealth**](Mks2ComponentHealth.md) |  | [optional] 
**konnectivity** | [**Mks2ComponentHealth**](Mks2ComponentHealth.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.mks2_network_health import Mks2NetworkHealth

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2NetworkHealth from a JSON string
mks2_network_health_instance = Mks2NetworkHealth.from_json(json)
# print the JSON string representation of the object
print(Mks2NetworkHealth.to_json())

# convert the object into a dict
mks2_network_health_dict = mks2_network_health_instance.to_dict()
# create an instance of Mks2NetworkHealth from a dict
mks2_network_health_from_dict = Mks2NetworkHealth.from_dict(mks2_network_health_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


