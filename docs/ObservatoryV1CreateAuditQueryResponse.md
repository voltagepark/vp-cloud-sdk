# ObservatoryV1CreateAuditQueryResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**coverage** | [**ObservatoryV1AuditCoverage**](ObservatoryV1AuditCoverage.md) |  | [optional] 
**query_id** | **str** |  | [optional] 
**state** | [**ObservatoryV1AuditQueryState**](ObservatoryV1AuditQueryState.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_create_audit_query_response import ObservatoryV1CreateAuditQueryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1CreateAuditQueryResponse from a JSON string
observatory_v1_create_audit_query_response_instance = ObservatoryV1CreateAuditQueryResponse.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1CreateAuditQueryResponse.to_json())

# convert the object into a dict
observatory_v1_create_audit_query_response_dict = observatory_v1_create_audit_query_response_instance.to_dict()
# create an instance of ObservatoryV1CreateAuditQueryResponse from a dict
observatory_v1_create_audit_query_response_from_dict = ObservatoryV1CreateAuditQueryResponse.from_dict(observatory_v1_create_audit_query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


