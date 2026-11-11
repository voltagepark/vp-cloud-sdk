# ModifyStorageRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**storage_views** | [**List[ModifyStorageRequestStorageViewsInner]**](ModifyStorageRequestStorageViewsInner.md) | List of storage views to modify. Must match the existing storage configuration: same number of items and same mount points. Only the size values can be changed. | 

## Example

```python
from vpcloud_client.models.modify_storage_request import ModifyStorageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ModifyStorageRequest from a JSON string
modify_storage_request_instance = ModifyStorageRequest.from_json(json)
# print the JSON string representation of the object
print(ModifyStorageRequest.to_json())

# convert the object into a dict
modify_storage_request_dict = modify_storage_request_instance.to_dict()
# create an instance of ModifyStorageRequest from a dict
modify_storage_request_from_dict = ModifyStorageRequest.from_dict(modify_storage_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


