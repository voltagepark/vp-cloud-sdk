# ObservatoryV1AuditQueryStatistics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bytes_scanned** | **str** | Bytes of audit log the query scanned, as a decimal string. | [optional] 
**event_count** | **int** | Events in the results. Set once the query has succeeded. | [optional] 
**truncated** | **bool** | True when more events matched than the results hold. Narrow the time window or the filters. | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_audit_query_statistics import ObservatoryV1AuditQueryStatistics

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1AuditQueryStatistics from a JSON string
observatory_v1_audit_query_statistics_instance = ObservatoryV1AuditQueryStatistics.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1AuditQueryStatistics.to_json())

# convert the object into a dict
observatory_v1_audit_query_statistics_dict = observatory_v1_audit_query_statistics_instance.to_dict()
# create an instance of ObservatoryV1AuditQueryStatistics from a dict
observatory_v1_audit_query_statistics_from_dict = ObservatoryV1AuditQueryStatistics.from_dict(observatory_v1_audit_query_statistics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


