# vpcloud_client.AuditApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_audit_log_export**](AuditApi.md#get_audit_log_export) | **GET** /v1/audit-logs/export | Check the 90-day audit log export and get its download URL
[**get_audit_logs**](AuditApi.md#get_audit_logs) | **GET** /v1/audit-logs | List recent audit logs for your organization
[**start_audit_log_export**](AuditApi.md#start_audit_log_export) | **POST** /v1/audit-logs/export | Start building the 90-day audit log export for your organization


# **get_audit_log_export**
> AuditLogExportStatusResponse get_audit_log_export()

Check the 90-day audit log export and get its download URL

Reports the state of your organization's 90-day audit export and, once it is `ready`, returns a short-lived presigned download URL. Start an export with `POST /v1/audit-logs/export` first; this endpoint only reports and never starts one, so it is safe to poll.

**Statuses:**
- `notStarted` — no archive exists for today's window and no build is running. Call `POST` to start one.
- `running` — a build is in progress. Poll again in a few seconds.
- `ready` — the archive is complete; `url` and `expiresAt` are present.
- `failed` — the build did not finish; `error` carries a short reason. Call `POST` to try again.

**Format:** gzip-compressed NDJSON (`.ndjson.gz`) — one audit event per line, oldest first.

**Note:** the returned `url` expires within minutes — download promptly, and call this endpoint again for a fresh URL if it lapses. The archive itself persists for the rest of the UTC day. Actions taken by Voltage Park support/admin staff are attributed to their own organization and are not included here.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.audit_log_export_status_response import AuditLogExportStatusResponse
from vpcloud_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.sea1.voltagepark.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vpcloud_client.Configuration(
    host = "https://api.sea1.voltagepark.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = vpcloud_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with vpcloud_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vpcloud_client.AuditApi(api_client)

    try:
        # Check the 90-day audit log export and get its download URL
        api_response = api_instance.get_audit_log_export()
        print("The response of AuditApi->get_audit_log_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuditApi->get_audit_log_export: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AuditLogExportStatusResponse**](AuditLogExportStatusResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The current state of your organization&#39;s 90-day export, including a presigned download URL when it is ready. |  -  |
**401** | Unauthenticated - missing or invalid token |  -  |
**403** | Authenticated but not permitted to export audit logs |  -  |
**500** | Internal server error before the status could be read (for example, audit export is not configured for this deployment) |  -  |
**502** | An upstream dependency failed while reading the export status or minting the download URL (object storage was unreachable) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_audit_logs**
> AuditLogListResponse get_audit_logs()

List recent audit logs for your organization

Returns the most recent audit events for the authenticated caller's organization — who did what, when, and from where. Scoped automatically to your organization (derived from your token); you cannot query another organization's activity.

**When to use:**
- Let an organization owner review what users in their org have been doing
- Investigate recent access or changes across your fleets

**Scope & limits (beta preview):**
- Returns up to the 100 most recent events, newest first.
- Covers recent activity only (a bounded lookback window).
- No filtering or pagination yet — this is a preview feature and the contract may change.

**Note:** Actions taken by Voltage Park support/admin staff are attributed to their own organization and are not included here.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.audit_log_list_response import AuditLogListResponse
from vpcloud_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.sea1.voltagepark.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vpcloud_client.Configuration(
    host = "https://api.sea1.voltagepark.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = vpcloud_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with vpcloud_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vpcloud_client.AuditApi(api_client)

    try:
        # List recent audit logs for your organization
        api_response = api_instance.get_audit_logs()
        print("The response of AuditApi->get_audit_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuditApi->get_audit_logs: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AuditLogListResponse**](AuditLogListResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The most recent audit events for your organization (up to 100, newest first). Returns an empty list when there is no recent activity. |  -  |
**401** | Unauthenticated - missing or invalid token |  -  |
**500** | Internal server error before the audit query could run |  -  |
**502** | The upstream audit log store (CloudWatch) failed or timed out |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_audit_log_export**
> AuditLogExportStatusResponse start_audit_log_export()

Start building the 90-day audit log export for your organization

Starts preparing a downloadable archive of your organization's audit events for the trailing 90 days, and returns immediately — building it takes longer than a request can wait. Poll `GET /v1/audit-logs/export` until `status` is `ready`, then download the `url` it returns. Scoped automatically to your organization (derived from your token); you cannot export another organization's activity.

**When to use:**
- Produce 90 days of audit evidence for a SOC 2 or customer security review
- Retain or analyze activity beyond the recent-events endpoint's bounded preview

**Window:** whole days only. The archive covers the 90 days ending at the most recent UTC midnight, so the current partial day is excluded and every caller on the same UTC day gets the identical archive. There are no parameters — the window is fixed, which is what makes the archive reusable.

**Idempotent:** safe to call repeatedly. If today's archive is already built this returns `ready` without doing any work; if a build is already running it returns `running` rather than starting a second one. At most one archive is built per organization per UTC day.

**Expect a wait** on the first call of a UTC day — typically under a minute, and longer for organizations with high activity. Subsequent calls the same day are immediate.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.audit_log_export_status_response import AuditLogExportStatusResponse
from vpcloud_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.sea1.voltagepark.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vpcloud_client.Configuration(
    host = "https://api.sea1.voltagepark.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = vpcloud_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with vpcloud_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vpcloud_client.AuditApi(api_client)

    try:
        # Start building the 90-day audit log export for your organization
        api_response = api_instance.start_audit_log_export()
        print("The response of AuditApi->start_audit_log_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuditApi->start_audit_log_export: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AuditLogExportStatusResponse**](AuditLogExportStatusResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Accepted. The response carries the current status: &#x60;running&#x60; when this call started the build (or found one already in progress), or &#x60;ready&#x60; when today&#39;s archive already existed and no work was needed. |  -  |
**401** | Unauthenticated - missing or invalid token |  -  |
**403** | Authenticated but not permitted to export audit logs |  -  |
**500** | Internal server error before the export could be started (for example, audit export is not configured for this deployment) |  -  |
**502** | An upstream dependency failed while starting the export (object storage was unreachable) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

