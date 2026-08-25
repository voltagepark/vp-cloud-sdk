# StorageViewListResponse

The set of physical VAST storage views for a fleet's reservation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[StorageView]**](StorageView.md) | Storage views. Empty array (not null) when none are provisioned. | 
**storage_pending** | **bool** | True when the fleet exists but its storage has not been materialized yet; in that case &#x60;items&#x60; is always empty. Omitted (or false) once storage is available. | [optional] 

## Example

```python
from vpcloud_client.models.storage_view_list_response import StorageViewListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StorageViewListResponse from a JSON string
storage_view_list_response_instance = StorageViewListResponse.from_json(json)
# print the JSON string representation of the object
print(StorageViewListResponse.to_json())

# convert the object into a dict
storage_view_list_response_dict = storage_view_list_response_instance.to_dict()
# create an instance of StorageViewListResponse from a dict
storage_view_list_response_from_dict = StorageViewListResponse.from_dict(storage_view_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


