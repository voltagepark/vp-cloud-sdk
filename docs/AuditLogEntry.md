# AuditLogEntry

A single audit event for an organization: who performed an operation, when, and from where. This is a curated, customer-facing subset of the internal audit record.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timestamp** | **datetime** | When the request completed (RFC 3339 / ISO 8601, UTC). | 
**user_id** | **str** | Identifier of the user (token subject) who made the request, when available. | [optional] 
**operation** | **str** | High-level operation name for the request (e.g., LIST_FLEETS, DELETE_FLEET). | 
**method** | **str** | HTTP method of the request (e.g., GET, POST, DELETE). | 
**route** | **str** | Matched route template for the request (e.g., &#39;GET /v1/fleets/{fleetId}&#39;). | 
**status_code** | **int** | HTTP status code returned for the request. | 
**auth_outcome** | **str** | Authorization outcome for the request (e.g., &#39;allowed&#39;, &#39;denied&#39;, &#39;unauthenticated&#39;). | [optional] 
**client_ip** | **str** | Best-effort client IP address the request originated from, when available. | [optional] 
**user_agent** | **str** | User-agent string reported by the client, when available. | [optional] 
**resource** | **str** | Concrete resource(s) the request acted on, flattened as comma-separated key&#x3D;value pairs (e.g. &#39;fleetId&#x3D;f-123&#39; or &#39;fleetId&#x3D;f-123,nodeId&#x3D;g001&#39;). Absent when the request targeted no specific resource. Whereas &#39;route&#39; shows the template, this shows the actual identifiers. | [optional] 

## Example

```python
from vpcloud_client.models.audit_log_entry import AuditLogEntry

# TODO update the JSON string below
json = "{}"
# create an instance of AuditLogEntry from a JSON string
audit_log_entry_instance = AuditLogEntry.from_json(json)
# print the JSON string representation of the object
print(AuditLogEntry.to_json())

# convert the object into a dict
audit_log_entry_dict = audit_log_entry_instance.to_dict()
# create an instance of AuditLogEntry from a dict
audit_log_entry_from_dict = AuditLogEntry.from_dict(audit_log_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


