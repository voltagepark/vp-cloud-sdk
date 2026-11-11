# vpcloud_client.ClusterValidationApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_cluster_validation_detail**](ClusterValidationApi.md#get_cluster_validation_detail) | **GET** /v1/fleets/{fleetId}/cluster-validation/{validationId}/details | Get cluster validation run details
[**get_cluster_validation_report**](ClusterValidationApi.md#get_cluster_validation_report) | **GET** /v1/fleets/{fleetId}/cluster-validation/{validationId}/report | Get cluster validation run report
[**list_cluster_validation_tests**](ClusterValidationApi.md#list_cluster_validation_tests) | **GET** /v1/fleets/{fleetId}/cluster-validation/tests | List available cluster validation tests
[**list_cluster_validations**](ClusterValidationApi.md#list_cluster_validations) | **GET** /v1/fleets/{fleetId}/cluster-validation | List recent cluster validation runs
[**trigger_cluster_validation**](ClusterValidationApi.md#trigger_cluster_validation) | **POST** /v1/fleets/{fleetId}/cluster-validation | Start a cluster validation run


# **get_cluster_validation_detail**
> ClusterValidationDetail get_cluster_validation_detail(fleet_id, validation_id)

Get cluster validation run details

Returns the full detail for a specific cluster-validation run on your fleet: run state, the node names included, whether it was a Kubernetes-aware run, and timestamps.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.cluster_validation_detail import ClusterValidationDetail
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
    api_instance = vpcloud_client.ClusterValidationApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    validation_id = 56 # int | Cluster-validation run id (from the trigger or list response).

    try:
        # Get cluster validation run details
        api_response = api_instance.get_cluster_validation_detail(fleet_id, validation_id)
        print("The response of ClusterValidationApi->get_cluster_validation_detail:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClusterValidationApi->get_cluster_validation_detail: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **validation_id** | **int**| Cluster-validation run id (from the trigger or list response). | 

### Return type

[**ClusterValidationDetail**](ClusterValidationDetail.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cluster-validation run detail |  -  |
**400** | Fleet does not support cluster validation, or the validation id is invalid |  -  |
**401** | Authentication required |  -  |
**404** | Fleet or validation run not found |  -  |
**500** | Internal server error |  -  |
**502** | Upstream service returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cluster_validation_report**
> Dict[str, object] get_cluster_validation_report(fleet_id, validation_id)

Get cluster validation run report

Returns the per-node pass/fail report for a specific cluster-validation run on your fleet, including a summary for each result. When a result has no summary available (for example, a test that could not run), a generic message is returned in its place.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
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
    api_instance = vpcloud_client.ClusterValidationApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    validation_id = 56 # int | Cluster-validation run id (from the trigger or list response).

    try:
        # Get cluster validation run report
        api_response = api_instance.get_cluster_validation_report(fleet_id, validation_id)
        print("The response of ClusterValidationApi->get_cluster_validation_report:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClusterValidationApi->get_cluster_validation_report: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **validation_id** | **int**| Cluster-validation run id (from the trigger or list response). | 

### Return type

**Dict[str, object]**

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cluster-validation report |  -  |
**400** | Fleet does not support cluster validation, or the validation id is invalid |  -  |
**401** | Authentication required |  -  |
**404** | Fleet or validation run not found |  -  |
**500** | Internal server error |  -  |
**502** | Upstream service returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_cluster_validation_tests**
> Dict[str, object] list_cluster_validation_tests(fleet_id)

List available cluster validation tests

Lists the cluster-validation tests available for your fleet, grouped by category, each with a short description. Which tests are returned depends on the fleet's type.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
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
    api_instance = vpcloud_client.ClusterValidationApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier

    try:
        # List available cluster validation tests
        api_response = api_instance.list_cluster_validation_tests(fleet_id)
        print("The response of ClusterValidationApi->list_cluster_validation_tests:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClusterValidationApi->list_cluster_validation_tests: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

**Dict[str, object]**

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Available cluster-validation tests grouped by category |  -  |
**401** | Authentication required |  -  |
**404** | Fleet not found |  -  |
**500** | Internal server error |  -  |
**502** | Upstream service returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_cluster_validations**
> ClusterValidationListResponse list_cluster_validations(fleet_id)

List recent cluster validation runs

Returns up to the 10 most recent cluster-validation runs for your fleet, newest first.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.cluster_validation_list_response import ClusterValidationListResponse
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
    api_instance = vpcloud_client.ClusterValidationApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier

    try:
        # List recent cluster validation runs
        api_response = api_instance.list_cluster_validations(fleet_id)
        print("The response of ClusterValidationApi->list_cluster_validations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClusterValidationApi->list_cluster_validations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

[**ClusterValidationListResponse**](ClusterValidationListResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Recent cluster-validation runs (max 10, newest first). |  -  |
**400** | Fleet does not support cluster validation |  -  |
**401** | Authentication required |  -  |
**404** | Fleet not found |  -  |
**500** | Internal server error |  -  |
**502** | Upstream service returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **trigger_cluster_validation**
> ClusterValidationResponse trigger_cluster_validation(fleet_id, idempotency_key=idempotency_key, customer_trigger_cluster_validation_request=customer_trigger_cluster_validation_request)

Start a cluster validation run

Starts a cluster-validation run against your fleet's nodes and returns the run id (use it to poll status, view details, or fetch the report). Runs are always multi-host. An optional node subset and an optional list of tests (from the test catalog) are honored; omit the tests to run the default set. Kubernetes-aware runs require a Kubernetes-enabled fleet; the required cluster credential is obtained automatically.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.cluster_validation_response import ClusterValidationResponse
from vpcloud_client.models.customer_trigger_cluster_validation_request import CustomerTriggerClusterValidationRequest
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
    api_instance = vpcloud_client.ClusterValidationApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns `422 Unprocessable Entity` - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Key reuse: Returns `422 Unprocessable Entity` when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.sea1.voltagepark.com/v1/sshkeys',             json=ssh_key,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key # Same key for retries             }         )                  if response.status_code == 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception('Max retries exceeded') ``` (optional)
    customer_trigger_cluster_validation_request = vpcloud_client.CustomerTriggerClusterValidationRequest() # CustomerTriggerClusterValidationRequest | Optional run parameters. Omit the body to validate all fleet nodes with the default set of tests. (optional)

    try:
        # Start a cluster validation run
        api_response = api_instance.trigger_cluster_validation(fleet_id, idempotency_key=idempotency_key, customer_trigger_cluster_validation_request=customer_trigger_cluster_validation_request)
        print("The response of ClusterValidationApi->trigger_cluster_validation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClusterValidationApi->trigger_cluster_validation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns &#x60;422 Unprocessable Entity&#x60; - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Key reuse: Returns &#x60;422 Unprocessable Entity&#x60; when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.sea1.voltagepark.com/v1/sshkeys&#39;,             json&#x3D;ssh_key,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60; | [optional] 
 **customer_trigger_cluster_validation_request** | [**CustomerTriggerClusterValidationRequest**](CustomerTriggerClusterValidationRequest.md)| Optional run parameters. Omit the body to validate all fleet nodes with the default set of tests. | [optional] 

### Return type

[**ClusterValidationResponse**](ClusterValidationResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Validation run accepted and started. |  -  |
**400** | Fleet does not support cluster validation, or the request is invalid |  -  |
**401** | Authentication required |  -  |
**404** | Fleet not found |  -  |
**409** | A cluster validation is already running for this fleet |  -  |
**412** | GPU validation has not finished on one or more of the target nodes, so the run cannot start. The message names each node and its state. Retry once validation has finished on those nodes, or leave them out of the run with &#x60;nodeNames&#x60;. If a node failed GPU validation or stays blocked, contact support. |  -  |
**500** | Internal server error |  -  |
**502** | Upstream service returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

