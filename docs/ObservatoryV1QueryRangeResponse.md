# ObservatoryV1QueryRangeResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | [**ObservatoryV1MetricsResult**](ObservatoryV1MetricsResult.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_query_range_response import ObservatoryV1QueryRangeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1QueryRangeResponse from a JSON string
observatory_v1_query_range_response_instance = ObservatoryV1QueryRangeResponse.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1QueryRangeResponse.to_json())

# convert the object into a dict
observatory_v1_query_range_response_dict = observatory_v1_query_range_response_instance.to_dict()
# create an instance of ObservatoryV1QueryRangeResponse from a dict
observatory_v1_query_range_response_from_dict = ObservatoryV1QueryRangeResponse.from_dict(observatory_v1_query_range_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


