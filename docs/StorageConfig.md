# StorageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mount_point** | **str** | Mount point for storage | 
**size** | **int** | Storage size in bytes | 

## Example

```python
from vpcloud_client.models.storage_config import StorageConfig

# a StorageConfig as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of StorageConfig from a JSON string
storage_config_instance = StorageConfig.from_json(json)
# print the JSON string representation of the object
print(storage_config_instance.to_json())

# convert the object into a dict
storage_config_dict = storage_config_instance.to_dict()
# create an instance of StorageConfig from a dict
storage_config_from_dict = StorageConfig.from_dict(storage_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


