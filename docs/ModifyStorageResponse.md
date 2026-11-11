# ModifyStorageResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fleet_id** | **str** | Unique identifier for the fleet | 
**status** | **str** | Status of the storage modification operation | 
**message** | **str** | Descriptive message about the operation | 

## Example

```python
from vpcloud_client.models.modify_storage_response import ModifyStorageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ModifyStorageResponse from a JSON string
modify_storage_response_instance = ModifyStorageResponse.from_json(json)
# print the JSON string representation of the object
print(ModifyStorageResponse.to_json())

# convert the object into a dict
modify_storage_response_dict = modify_storage_response_instance.to_dict()
# create an instance of ModifyStorageResponse from a dict
modify_storage_response_from_dict = ModifyStorageResponse.from_dict(modify_storage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


