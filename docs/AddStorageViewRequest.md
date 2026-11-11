# AddStorageViewRequest

Request to add a new physical VAST storage view to a fleet's reservation. At least one quota field (`size`, `hardLimit`, or `softLimit`+`hardLimit`) is required. Accepted quota shapes: (1) `size` alone, (2) `hardLimit` alone (treated as an alias for `size`; the soft quota is then set to 90% automatically), or (3) `softLimit`+`hardLimit` together (or `softLimit`+`size`, since `size` and `hardLimit` are aliases). `softLimit` on its own is rejected. If both `size` and `hardLimit` are supplied they must be equal.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mount_point** | **str** | Mount point for the new storage view. One path segment under &#39;/&#39;, charset [a-zA-Z0-9_-], max 128 characters. | 
**size** | **int** | Provisioned size in bytes. Must be a positive multiple of 1 MiB (1048576 bytes). May be supplied on its own (the soft quota is then set to 90% of size automatically); when supplied together with &#x60;hardLimit&#x60;, the two must be equal. | [optional] 
**soft_limit** | **int** | Soft quota in bytes. Must be a positive multiple of 1 MiB (1048576 bytes) and less than or equal to the hard quota. Must be supplied together with &#x60;hardLimit&#x60; (or with &#x60;size&#x60; acting as the hard quota). | [optional] 
**hard_limit** | **int** | Hard quota in bytes. Must be a positive multiple of 1 MiB (1048576 bytes). May be supplied on its own (treated as an alias for &#x60;size&#x60;; the soft quota is then set to 90% automatically) or together with &#x60;softLimit&#x60;. When supplied together with &#x60;size&#x60;, the two must be equal. | [optional] 
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


