# ModifyStorageRequestStorageViewsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mount_point** | **str** | Mount point for the storage view (e.g., &#39;/data&#39;, &#39;/home&#39;) | 
**size** | **int** | Storage size in bytes (maximum: 1PB &#x3D; 1,125,899,906,842,624 bytes) | 

## Example

```python
from vpcloud_client.models.modify_storage_request_storage_views_inner import ModifyStorageRequestStorageViewsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ModifyStorageRequestStorageViewsInner from a JSON string
modify_storage_request_storage_views_inner_instance = ModifyStorageRequestStorageViewsInner.from_json(json)
# print the JSON string representation of the object
print(ModifyStorageRequestStorageViewsInner.to_json())

# convert the object into a dict
modify_storage_request_storage_views_inner_dict = modify_storage_request_storage_views_inner_instance.to_dict()
# create an instance of ModifyStorageRequestStorageViewsInner from a dict
modify_storage_request_storage_views_inner_from_dict = ModifyStorageRequestStorageViewsInner.from_dict(modify_storage_request_storage_views_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


