# ObservatoryV1CancelAuditQueryResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**state** | [**ObservatoryV1AuditQueryState**](ObservatoryV1AuditQueryState.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_cancel_audit_query_response import ObservatoryV1CancelAuditQueryResponse

# a ObservatoryV1CancelAuditQueryResponse as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of ObservatoryV1CancelAuditQueryResponse from a JSON string
observatory_v1_cancel_audit_query_response_instance = ObservatoryV1CancelAuditQueryResponse.from_json(json)
# print the JSON string representation of the object
print(observatory_v1_cancel_audit_query_response_instance.to_json())

# convert the object into a dict
observatory_v1_cancel_audit_query_response_dict = observatory_v1_cancel_audit_query_response_instance.to_dict()
# create an instance of ObservatoryV1CancelAuditQueryResponse from a dict
observatory_v1_cancel_audit_query_response_from_dict = ObservatoryV1CancelAuditQueryResponse.from_dict(observatory_v1_cancel_audit_query_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


