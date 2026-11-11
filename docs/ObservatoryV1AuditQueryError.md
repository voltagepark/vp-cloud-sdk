# ObservatoryV1AuditQueryError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | [**GoogleRpcCode**](GoogleRpcCode.md) |  | [optional] 
**message** | **str** |  | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_audit_query_error import ObservatoryV1AuditQueryError

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1AuditQueryError from a JSON string
observatory_v1_audit_query_error_instance = ObservatoryV1AuditQueryError.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1AuditQueryError.to_json())

# convert the object into a dict
observatory_v1_audit_query_error_dict = observatory_v1_audit_query_error_instance.to_dict()
# create an instance of ObservatoryV1AuditQueryError from a dict
observatory_v1_audit_query_error_from_dict = ObservatoryV1AuditQueryError.from_dict(observatory_v1_audit_query_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


