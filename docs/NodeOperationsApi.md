# vpcloud_client.NodeOperationsApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**remediate_nodes**](NodeOperationsApi.md#remediate_nodes) | **POST** /v1/fleets/{fleetId}/nodes/remediate | Fix unhealthy nodes


# **remediate_nodes**
> List[RemediateNodeResponse] remediate_nodes(fleet_id, remediate_node_request, idempotency_key=idempotency_key)

Fix unhealthy nodes

Request remediation for problematic nodes. The system will automatically restart, replace, or repair the specified nodes based on the issue.

**When to use:**
- Node is unresponsive or unhealthy
- GPU is malfunctioning
- Node has connectivity issues
- Need to force a node restart

**What happens:**
The system analyzes the issue and takes appropriate action (restart, replace, or repair). Specify the reason to help with diagnostics.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.remediate_node_request import RemediateNodeRequest
from vpcloud_client.models.remediate_node_response import RemediateNodeResponse
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
    api_instance = vpcloud_client.NodeOperationsApi(api_client)
    fleet_id = '900e8eac-2b1f-421f-a635-72556268b41f' # str | Fleet identifier
    remediate_node_request = [vpcloud_client.RemediateNodeRequest()] # List[RemediateNodeRequest] | 
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Body mismatch: Returns `422 Unprocessable Entity` (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.harbor.example.com/admin/fleets',             json=fleet_config,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key  # Same key for retries             }         )                  if response.status_code == 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code < 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception('Max retries exceeded') ```  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md (optional)

    try:
        # Fix unhealthy nodes
        api_response = api_instance.remediate_nodes(fleet_id, remediate_node_request, idempotency_key=idempotency_key)
        print("The response of NodeOperationsApi->remediate_nodes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NodeOperationsApi->remediate_nodes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **remediate_node_request** | [**List[RemediateNodeRequest]**](RemediateNodeRequest.md)|  | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Body mismatch: Returns &#x60;422 Unprocessable Entity&#x60; (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.harbor.example.com/admin/fleets&#39;,             json&#x3D;fleet_config,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key  # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code &lt; 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60;  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md | [optional] 

### Return type

[**List[RemediateNodeResponse]**](RemediateNodeResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Remediation request processed successfully |  -  |
**400** | Bad request - invalid remediation request |  -  |
**404** | Fleet not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

