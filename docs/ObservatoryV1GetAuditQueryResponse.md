# ObservatoryV1GetAuditQueryResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**coverage** | [**ObservatoryV1AuditCoverage**](ObservatoryV1AuditCoverage.md) |  | [optional] 
**error** | [**ObservatoryV1AuditQueryError**](ObservatoryV1AuditQueryError.md) |  | [optional] 
**state** | [**ObservatoryV1AuditQueryState**](ObservatoryV1AuditQueryState.md) |  | [optional] 
**statistics** | [**ObservatoryV1AuditQueryStatistics**](ObservatoryV1AuditQueryStatistics.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_get_audit_query_response import ObservatoryV1GetAuditQueryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1GetAuditQueryResponse from a JSON string
observatory_v1_get_audit_query_response_instance = ObservatoryV1GetAuditQueryResponse.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1GetAuditQueryResponse.to_json())

# convert the object into a dict
observatory_v1_get_audit_query_response_dict = observatory_v1_get_audit_query_response_instance.to_dict()
# create an instance of ObservatoryV1GetAuditQueryResponse from a dict
observatory_v1_get_audit_query_response_from_dict = ObservatoryV1GetAuditQueryResponse.from_dict(observatory_v1_get_audit_query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


