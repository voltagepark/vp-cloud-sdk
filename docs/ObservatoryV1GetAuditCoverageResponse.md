# ObservatoryV1GetAuditCoverageResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**coverage** | [**ObservatoryV1AuditCoverage**](ObservatoryV1AuditCoverage.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_get_audit_coverage_response import ObservatoryV1GetAuditCoverageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1GetAuditCoverageResponse from a JSON string
observatory_v1_get_audit_coverage_response_instance = ObservatoryV1GetAuditCoverageResponse.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1GetAuditCoverageResponse.to_json())

# convert the object into a dict
observatory_v1_get_audit_coverage_response_dict = observatory_v1_get_audit_coverage_response_instance.to_dict()
# create an instance of ObservatoryV1GetAuditCoverageResponse from a dict
observatory_v1_get_audit_coverage_response_from_dict = ObservatoryV1GetAuditCoverageResponse.from_dict(observatory_v1_get_audit_coverage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


