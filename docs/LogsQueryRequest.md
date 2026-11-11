# LogsQueryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**end** | **datetime** |  | [optional] 
**limit** | **int** | Maximum number of lines to return. | [optional] 
**query** | **str** | LogsQL, evaluated as sent. | [optional] 
**start** | **datetime** |  | [optional] 

## Example

```python
from vpcloud_client.models.logs_query_request import LogsQueryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LogsQueryRequest from a JSON string
logs_query_request_instance = LogsQueryRequest.from_json(json)
# print the JSON string representation of the object
print(LogsQueryRequest.to_json())

# convert the object into a dict
logs_query_request_dict = logs_query_request_instance.to_dict()
# create an instance of LogsQueryRequest from a dict
logs_query_request_from_dict = LogsQueryRequest.from_dict(logs_query_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


