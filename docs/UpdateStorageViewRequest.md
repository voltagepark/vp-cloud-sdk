# UpdateStorageViewRequest

Request to update the size/quotas of an existing physical VAST storage view. The mount point is taken from the URL path.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | **int** | New provisioned size in bytes. | [optional] 
**soft_limit** | **int** | New soft quota in bytes. | [optional] 
**hard_limit** | **int** | New hard quota in bytes. | [optional] 

## Example

```python
from vpcloud_client.models.update_storage_view_request import UpdateStorageViewRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateStorageViewRequest from a JSON string
update_storage_view_request_instance = UpdateStorageViewRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateStorageViewRequest.to_json())

# convert the object into a dict
update_storage_view_request_dict = update_storage_view_request_instance.to_dict()
# create an instance of UpdateStorageViewRequest from a dict
update_storage_view_request_from_dict = UpdateStorageViewRequest.from_dict(update_storage_view_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


