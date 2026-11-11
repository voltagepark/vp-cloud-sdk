# ObservatoryV1LogsQueryResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**lines_json** | **List[bytearray]** | The matching lines, each the base64 of one JSON log record. | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_logs_query_response import ObservatoryV1LogsQueryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1LogsQueryResponse from a JSON string
observatory_v1_logs_query_response_instance = ObservatoryV1LogsQueryResponse.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1LogsQueryResponse.to_json())

# convert the object into a dict
observatory_v1_logs_query_response_dict = observatory_v1_logs_query_response_instance.to_dict()
# create an instance of ObservatoryV1LogsQueryResponse from a dict
observatory_v1_logs_query_response_from_dict = ObservatoryV1LogsQueryResponse.from_dict(observatory_v1_logs_query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


