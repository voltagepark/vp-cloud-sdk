# Infrastructure


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**network** | [**InfrastructureNetwork**](InfrastructureNetwork.md) |  | 
**vast** | [**List[StorageConfig]**](StorageConfig.md) | Storage configuration | [optional] 

## Example

```python
from vpcloud_client.models.infrastructure import Infrastructure

# a Infrastructure as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of Infrastructure from a JSON string
infrastructure_instance = Infrastructure.from_json(json)
# print the JSON string representation of the object
print(infrastructure_instance.to_json())

# convert the object into a dict
infrastructure_dict = infrastructure_instance.to_dict()
# create an instance of Infrastructure from a dict
infrastructure_from_dict = Infrastructure.from_dict(infrastructure_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


