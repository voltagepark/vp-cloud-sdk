# CreateAuditQueryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_groups** | **List[str]** |  | [optional] 
**audit_ids** | **List[str]** |  | [optional] 
**end** | **datetime** |  | [optional] 
**names** | **List[str]** | Keep only events on objects with one of these names. | [optional] 
**namespaces** | **List[str]** | Keep only events in one of these namespaces. | [optional] 
**order** | [**ObservatoryV1AuditOrder**](ObservatoryV1AuditOrder.md) |  | [optional] 
**request_id** | **str** | Identifies this request. Retrying with the same requestId returns the same query rather than starting another. A new one is generated when omitted. | [optional] 
**resources** | **List[str]** | Keep only events on one of these resources, for example \&quot;deployments\&quot;. | [optional] 
**response_codes** | **List[int]** |  | [optional] 
**source_ips** | **List[str]** |  | [optional] 
**stages** | **List[str]** |  | [optional] 
**start** | **datetime** |  | [optional] 
**usernames** | **List[str]** | Keep only events by one of these users. | [optional] 
**verbs** | **List[str]** | Keep only events with one of these verbs, for example \&quot;delete\&quot;. | [optional] 

## Example

```python
from vpcloud_client.models.create_audit_query_request import CreateAuditQueryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAuditQueryRequest from a JSON string
create_audit_query_request_instance = CreateAuditQueryRequest.from_json(json)
# print the JSON string representation of the object
print(CreateAuditQueryRequest.to_json())

# convert the object into a dict
create_audit_query_request_dict = create_audit_query_request_instance.to_dict()
# create an instance of CreateAuditQueryRequest from a dict
create_audit_query_request_from_dict = CreateAuditQueryRequest.from_dict(create_audit_query_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


