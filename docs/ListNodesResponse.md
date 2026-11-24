# ListNodesResponse

Response containing a list of nodes with optional pagination metadata

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**nodes** | [**List[Node]**](Node.md) | List of nodes in the fleet | 
**next_token** | **str** | Pagination token to retrieve the next page of results. Null when no more pages available. | [optional] 
**limit** | **int** | Number of items requested per page. Null when pagination not used. | [optional] 

## Example

```python
from vpcloud_client.models.list_nodes_response import ListNodesResponse

# a ListNodesResponse as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of ListNodesResponse from a JSON string
list_nodes_response_instance = ListNodesResponse.from_json(json)
# print the JSON string representation of the object
print(list_nodes_response_instance.to_json())

# convert the object into a dict
list_nodes_response_dict = list_nodes_response_instance.to_dict()
# create an instance of ListNodesResponse from a dict
list_nodes_response_from_dict = ListNodesResponse.from_dict(list_nodes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


