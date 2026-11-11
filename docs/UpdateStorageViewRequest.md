# UpdateStorageViewRequest

Request to update the size/quotas of an existing physical VAST storage view. The mount point is taken from the URL path. At least one of `size`, `hardLimit`, `softLimit` is required. Accepted quota shapes: (1) `size` alone, (2) `hardLimit` alone (treated as an alias for `size`; the soft quota is then reset to 90% automatically), or (3) `softLimit`+`hardLimit` together (or `softLimit`+`size`, since `size` and `hardLimit` are aliases). `softLimit` on its own is rejected. If both `size` and `hardLimit` are supplied they must be equal.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | **int** | New provisioned size in bytes. Must be a positive multiple of 1 MiB (1048576 bytes). May be supplied on its own (resets the soft quota to 90% of size); when supplied together with &#x60;hardLimit&#x60;, the two must be equal. | [optional] 
**soft_limit** | **int** | New soft quota in bytes. Must be a positive multiple of 1 MiB (1048576 bytes) and less than or equal to the hard quota. Must be supplied together with &#x60;hardLimit&#x60; (or with &#x60;size&#x60; acting as the hard quota). | [optional] 
**hard_limit** | **int** | New hard quota in bytes. Must be a positive multiple of 1 MiB (1048576 bytes). May be supplied on its own (treated as an alias for &#x60;size&#x60;; the soft quota is then reset to 90% automatically) or together with &#x60;softLimit&#x60;. When supplied together with &#x60;size&#x60;, the two must be equal. | [optional] 

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


