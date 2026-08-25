# AuditLogExportStatusResponse

State of the caller's 90-day audit export: which window it covers, whether the archive is ready, and - once it is - a short-lived presigned download URL.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | Where the export stands. &#39;notStarted&#39;: no archive for today&#39;s window and nothing running - POST to start one. &#39;running&#39;: a build is in progress, poll again in a few seconds. &#39;ready&#39;: the archive is complete and &#39;url&#39; is present. &#39;failed&#39;: the build did not finish, see &#39;error&#39;, and POST to retry.  **Which operation returns which:** POST only ever returns &#39;running&#39; or &#39;ready&#39; - starting an export always leaves it in one of those two states. All four are possible from GET. &#39;notStarted&#39; is therefore GET-only, and you will see it when you check before any export has been requested, and again after each UTC midnight, when the previous day&#39;s archive no longer covers the current window. | 
**window_start** | **datetime** | Inclusive start of the exported window: a UTC midnight, 90 days before &#39;windowEnd&#39;. | 
**window_end** | **datetime** | Exclusive end of the exported window: the most recent UTC midnight. The current partial day is not included. | 
**format** | **str** | Archive encoding: gzip-compressed newline-delimited JSON, one audit event per line. | 
**url** | **str** | Presigned HTTPS URL for the gzipped NDJSON archive. Present only when &#39;status&#39; is &#39;ready&#39;. Treat it as a credential: anyone holding it can download the archive until it expires. | [optional] 
**expires_at** | **datetime** | When &#39;url&#39; stops working (RFC 3339 / ISO 8601, UTC). Present only when &#39;status&#39; is &#39;ready&#39;. Minutes, not hours - call the endpoint again for a fresh URL. The archive itself outlives the URL. | [optional] 
**started_at** | **datetime** | When the current (or most recent) build started. Absent when &#39;status&#39; is &#39;notStarted&#39;. | [optional] 
**completed_at** | **datetime** | When the build finished, successfully or not. Present only when &#39;status&#39; is &#39;ready&#39; or &#39;failed&#39;. | [optional] 
**error** | **str** | Short, non-sensitive reason the build failed. Present only when &#39;status&#39; is &#39;failed&#39;. | [optional] 

## Example

```python
from vpcloud_client.models.audit_log_export_status_response import AuditLogExportStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AuditLogExportStatusResponse from a JSON string
audit_log_export_status_response_instance = AuditLogExportStatusResponse.from_json(json)
# print the JSON string representation of the object
print(AuditLogExportStatusResponse.to_json())

# convert the object into a dict
audit_log_export_status_response_dict = audit_log_export_status_response_instance.to_dict()
# create an instance of AuditLogExportStatusResponse from a dict
audit_log_export_status_response_from_dict = AuditLogExportStatusResponse.from_dict(audit_log_export_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


