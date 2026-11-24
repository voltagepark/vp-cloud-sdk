# ExternalStorageConfig

External storage configuration

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mount_path** | **str** | Mount path for the external storage | 
**size** | **str** | Storage size | 

## Example

```python
from vpcloud_client.models.external_storage_config import ExternalStorageConfig

# a ExternalStorageConfig as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of ExternalStorageConfig from a JSON string
external_storage_config_instance = ExternalStorageConfig.from_json(json)
# print the JSON string representation of the object
print(external_storage_config_instance.to_json())

# convert the object into a dict
external_storage_config_dict = external_storage_config_instance.to_dict()
# create an instance of ExternalStorageConfig from a dict
external_storage_config_from_dict = ExternalStorageConfig.from_dict(external_storage_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


