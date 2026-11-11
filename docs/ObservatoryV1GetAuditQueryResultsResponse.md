# ObservatoryV1GetAuditQueryResultsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**events_json** | **List[bytearray]** | Audit events, each the base64 of one audit.k8s.io/v1 Event exactly as recorded. | [optional] 
**next_page_token** | **str** | Pass as pageToken to read the next page. Empty on the last page. | [optional] 
**truncated** | **bool** |  | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_get_audit_query_results_response import ObservatoryV1GetAuditQueryResultsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1GetAuditQueryResultsResponse from a JSON string
observatory_v1_get_audit_query_results_response_instance = ObservatoryV1GetAuditQueryResultsResponse.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1GetAuditQueryResultsResponse.to_json())

# convert the object into a dict
observatory_v1_get_audit_query_results_response_dict = observatory_v1_get_audit_query_results_response_instance.to_dict()
# create an instance of ObservatoryV1GetAuditQueryResultsResponse from a dict
observatory_v1_get_audit_query_results_response_from_dict = ObservatoryV1GetAuditQueryResultsResponse.from_dict(observatory_v1_get_audit_query_results_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


