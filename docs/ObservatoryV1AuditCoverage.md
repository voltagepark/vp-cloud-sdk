# ObservatoryV1AuditCoverage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**first_archived_time** | **datetime** |  | [optional] 
**gaps** | [**List[ObservatoryV1AuditCoverageGap]**](ObservatoryV1AuditCoverageGap.md) |  | [optional] 
**measured_time** | **datetime** |  | [optional] 
**newest_archived_time** | **datetime** |  | [optional] 
**settled_time** | **datetime** |  | [optional] 
**verdict** | [**ObservatoryV1AuditCoverageVerdict**](ObservatoryV1AuditCoverageVerdict.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_audit_coverage import ObservatoryV1AuditCoverage

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1AuditCoverage from a JSON string
observatory_v1_audit_coverage_instance = ObservatoryV1AuditCoverage.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1AuditCoverage.to_json())

# convert the object into a dict
observatory_v1_audit_coverage_dict = observatory_v1_audit_coverage_instance.to_dict()
# create an instance of ObservatoryV1AuditCoverage from a dict
observatory_v1_audit_coverage_from_dict = ObservatoryV1AuditCoverage.from_dict(observatory_v1_audit_coverage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


