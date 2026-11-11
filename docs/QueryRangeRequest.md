# QueryRangeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**end** | **datetime** |  | [optional] 
**query** | **str** | PromQL, evaluated as sent. | [optional] 
**start** | **datetime** |  | [optional] 
**step** | **str** |  | [optional] 

## Example

```python
from vpcloud_client.models.query_range_request import QueryRangeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of QueryRangeRequest from a JSON string
query_range_request_instance = QueryRangeRequest.from_json(json)
# print the JSON string representation of the object
print(QueryRangeRequest.to_json())

# convert the object into a dict
query_range_request_dict = query_range_request_instance.to_dict()
# create an instance of QueryRangeRequest from a dict
query_range_request_from_dict = QueryRangeRequest.from_dict(query_range_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


