# ListFleetsResponse

Response containing a list of fleets with optional pagination metadata

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fleets** | [**List[Fleet]**](Fleet.md) | Array of fleet objects | 
**next_token** | **str** | Pagination token to retrieve the next page of results. Null when pagination not used or no more pages available. | [optional] 
**limit** | **int** | Number of items requested per page. Null when pagination not used. | [optional] 

## Example

```python
from vpcloud_client.models.list_fleets_response import ListFleetsResponse

# a ListFleetsResponse as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of ListFleetsResponse from a JSON string
list_fleets_response_instance = ListFleetsResponse.from_json(json)
# print the JSON string representation of the object
print(list_fleets_response_instance.to_json())

# convert the object into a dict
list_fleets_response_dict = list_fleets_response_instance.to_dict()
# create an instance of ListFleetsResponse from a dict
list_fleets_response_from_dict = ListFleetsResponse.from_dict(list_fleets_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


