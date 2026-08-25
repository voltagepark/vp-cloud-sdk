# AddStorageViewRequest

Request to add a new physical VAST storage view to a fleet's reservation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mount_point** | **str** | Mount point for the new storage view (e.g., &#39;/data&#39;). | 
**size** | **int** | Provisioned size in bytes. | [optional] 
**soft_limit** | **int** | Soft quota in bytes. | [optional] 
**hard_limit** | **int** | Hard quota in bytes. | [optional] 
**protection_policy** | [**StorageProtectionPolicy**](StorageProtectionPolicy.md) |  | [optional] 
**provision** | **bool** | Whether to trigger VAST provisioning after adding the view. Only applies when storage has not yet been provisioned. | [optional] [default to True]

## Example

```python
from vpcloud_client.models.add_storage_view_request import AddStorageViewRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddStorageViewRequest from a JSON string
add_storage_view_request_instance = AddStorageViewRequest.from_json(json)
# print the JSON string representation of the object
print(AddStorageViewRequest.to_json())

# convert the object into a dict
add_storage_view_request_dict = add_storage_view_request_instance.to_dict()
# create an instance of AddStorageViewRequest from a dict
add_storage_view_request_from_dict = AddStorageViewRequest.from_dict(add_storage_view_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


