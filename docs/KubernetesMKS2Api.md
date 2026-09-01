# vpcloud_client.KubernetesMKS2Api

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cordon_customer_mks2_worker_node**](KubernetesMKS2Api.md#cordon_customer_mks2_worker_node) | **POST** /v1/fleets/{fleetId}/kubernetes-v2/nodes/{nodeId}/cordon | Cordon an MKS-2 worker node
[**drain_customer_mks2_worker_node**](KubernetesMKS2Api.md#drain_customer_mks2_worker_node) | **POST** /v1/fleets/{fleetId}/kubernetes-v2/nodes/{nodeId}/drain | Drain an MKS-2 worker node
[**get_customer_mks2_worker_node**](KubernetesMKS2Api.md#get_customer_mks2_worker_node) | **GET** /v1/fleets/{fleetId}/kubernetes-v2/nodes/{nodeId} | Get MKS-2 worker node detail
[**list_customer_mks2_pods**](KubernetesMKS2Api.md#list_customer_mks2_pods) | **GET** /v1/fleets/{fleetId}/kubernetes-v2/pods | List MKS-2 pods
[**list_customer_mks2_worker_nodes**](KubernetesMKS2Api.md#list_customer_mks2_worker_nodes) | **GET** /v1/fleets/{fleetId}/kubernetes-v2/nodes | List MKS-2 worker nodes
[**uncordon_customer_mks2_worker_node**](KubernetesMKS2Api.md#uncordon_customer_mks2_worker_node) | **POST** /v1/fleets/{fleetId}/kubernetes-v2/nodes/{nodeId}/uncordon | Uncordon an MKS-2 worker node


# **cordon_customer_mks2_worker_node**
> Mks2CordonNodeResponse cordon_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key)

Cordon an MKS-2 worker node

Marks the node unschedulable so the scheduler stops placing new pods on it. Existing pods are left running (use drain to evict them). Org-scoped: the caller's JWT org must own the fleet. The node must be joined to the cluster; otherwise the request is rejected with 400. Idempotency: pass `Idempotency-Key` to make this safely retryable.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.mks2_cordon_node_response import Mks2CordonNodeResponse
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
    api_instance = vpcloud_client.KubernetesMKS2Api(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    node_id = 'node_id_example' # str | MKS-2 worker-node identifier (registry id)
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Body mismatch: Returns `422 Unprocessable Entity` (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.harbor.example.com/admin/fleets',             json=fleet_config,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key  # Same key for retries             }         )                  if response.status_code == 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code < 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception('Max retries exceeded') ```  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md (optional)

    try:
        # Cordon an MKS-2 worker node
        api_response = api_instance.cordon_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key)
        print("The response of KubernetesMKS2Api->cordon_customer_mks2_worker_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesMKS2Api->cordon_customer_mks2_worker_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| MKS-2 worker-node identifier (registry id) | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Body mismatch: Returns &#x60;422 Unprocessable Entity&#x60; (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.harbor.example.com/admin/fleets&#39;,             json&#x3D;fleet_config,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key  # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code &lt; 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60;  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md | [optional] 

### Return type

[**Mks2CordonNodeResponse**](Mks2CordonNodeResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Node cordoned (marked unschedulable) |  -  |
**400** | Fleet exists but is not MKS-2-backed, the node id is not a member of the fleet&#39;s bare-metal list, or upstream MKS-2 rejected the request (e.g. the node has not joined the cluster yet) |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org, or upstream MKS-2 has no cluster / no such node |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream MKS-2 returned 5xx |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **drain_customer_mks2_worker_node**
> Mks2DrainNodeResponse drain_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key, mks2_drain_node_request=mks2_drain_node_request)

Drain an MKS-2 worker node

Cordons the node and then evicts its pods (respecting PodDisruptionBudgets). Org-scoped: the caller's JWT org must own the fleet. The node must be joined to the cluster; otherwise the request is rejected with 400, or 409 if the cluster is currently restoring or deleting. The request body is optional; omit it to use the defaults. Idempotency: pass `Idempotency-Key` to make this safely retryable.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.mks2_drain_node_request import Mks2DrainNodeRequest
from vpcloud_client.models.mks2_drain_node_response import Mks2DrainNodeResponse
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
    api_instance = vpcloud_client.KubernetesMKS2Api(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    node_id = 'node_id_example' # str | MKS-2 worker-node identifier (registry id)
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Body mismatch: Returns `422 Unprocessable Entity` (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.harbor.example.com/admin/fleets',             json=fleet_config,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key  # Same key for retries             }         )                  if response.status_code == 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code < 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception('Max retries exceeded') ```  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md (optional)
    mks2_drain_node_request = vpcloud_client.Mks2DrainNodeRequest() # Mks2DrainNodeRequest |  (optional)

    try:
        # Drain an MKS-2 worker node
        api_response = api_instance.drain_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key, mks2_drain_node_request=mks2_drain_node_request)
        print("The response of KubernetesMKS2Api->drain_customer_mks2_worker_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesMKS2Api->drain_customer_mks2_worker_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| MKS-2 worker-node identifier (registry id) | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Body mismatch: Returns &#x60;422 Unprocessable Entity&#x60; (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.harbor.example.com/admin/fleets&#39;,             json&#x3D;fleet_config,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key  # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code &lt; 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60;  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md | [optional] 
 **mks2_drain_node_request** | [**Mks2DrainNodeRequest**](Mks2DrainNodeRequest.md)|  | [optional] 

### Return type

[**Mks2DrainNodeResponse**](Mks2DrainNodeResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Drain initiated (pods evicted) |  -  |
**400** | Fleet does not have a Kubernetes cluster, the node is not a member of the fleet, the request body is malformed, or the node has not joined the cluster |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in the caller&#39;s org, or the cluster or node was not found |  -  |
**409** | The cluster is currently restoring or deleting |  -  |
**500** | Internal server error |  -  |
**502** | Upstream service returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_mks2_worker_node**
> Mks2WorkerNodeDetail get_customer_mks2_worker_node(fleet_id, node_id)

Get MKS-2 worker node detail

Returns the full detail for a single worker node in the fleet's MKS-2 cluster, including Kubernetes conditions, GPU info, labels/annotations, and registration timestamps. Org-scoped: the caller's JWT org must own the fleet. Unlike the list endpoint (joined-only), this resolves registered-but-not-yet-joined nodes by id.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.mks2_worker_node_detail import Mks2WorkerNodeDetail
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
    api_instance = vpcloud_client.KubernetesMKS2Api(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    node_id = 'node_id_example' # str | MKS-2 worker-node identifier (registry id)

    try:
        # Get MKS-2 worker node detail
        api_response = api_instance.get_customer_mks2_worker_node(fleet_id, node_id)
        print("The response of KubernetesMKS2Api->get_customer_mks2_worker_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesMKS2Api->get_customer_mks2_worker_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| MKS-2 worker-node identifier (registry id) | 

### Return type

[**Mks2WorkerNodeDetail**](Mks2WorkerNodeDetail.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns the worker-node detail |  -  |
**400** | Fleet exists but is not MKS-2-backed, or upstream MKS-2 rejected the request as malformed |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org, or upstream MKS-2 has no cluster / no such node |  -  |
**500** | Internal failure before the upstream call (network unreachable, configuration, etc.) |  -  |
**502** | Upstream MKS-2 returned 5xx |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_customer_mks2_pods**
> Mks2PodList list_customer_mks2_pods(fleet_id, namespace=namespace, node_name=node_name, phase=phase, limit=limit, cursor=cursor)

List MKS-2 pods

Lists pods in the fleet's MKS-2 cluster. Org-scoped: the caller's JWT org must own the fleet. Supports optional filtering by namespace, node, and phase, plus opaque cursor pagination.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.mks2_pod_list import Mks2PodList
from vpcloud_client.models.mks2_pod_phase import Mks2PodPhase
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
    api_instance = vpcloud_client.KubernetesMKS2Api(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    namespace = 'namespace_example' # str | Filter to pods in this namespace. Omit to list across all namespaces. (optional)
    node_name = 'node_name_example' # str | Filter to pods scheduled on this node (Kubernetes node name). (optional)
    phase = vpcloud_client.Mks2PodPhase() # Mks2PodPhase | Filter to pods in this lifecycle phase. (optional)
    limit = 56 # int | Maximum number of pods to return per page (1-100). Defaults to the upstream page size when omitted. (optional)
    cursor = 'cursor_example' # str | Opaque pagination cursor from a previous response's meta.nextCursor. (optional)

    try:
        # List MKS-2 pods
        api_response = api_instance.list_customer_mks2_pods(fleet_id, namespace=namespace, node_name=node_name, phase=phase, limit=limit, cursor=cursor)
        print("The response of KubernetesMKS2Api->list_customer_mks2_pods:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesMKS2Api->list_customer_mks2_pods: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **namespace** | **str**| Filter to pods in this namespace. Omit to list across all namespaces. | [optional] 
 **node_name** | **str**| Filter to pods scheduled on this node (Kubernetes node name). | [optional] 
 **phase** | [**Mks2PodPhase**](.md)| Filter to pods in this lifecycle phase. | [optional] 
 **limit** | **int**| Maximum number of pods to return per page (1-100). Defaults to the upstream page size when omitted. | [optional] 
 **cursor** | **str**| Opaque pagination cursor from a previous response&#39;s meta.nextCursor. | [optional] 

### Return type

[**Mks2PodList**](Mks2PodList.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns the pod list |  -  |
**400** | Fleet exists but is not MKS-2-backed, or upstream MKS-2 rejected the request as malformed |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org, or upstream MKS-2 has no cluster for the resolved id |  -  |
**500** | Internal failure before the upstream call (network unreachable, configuration, etc.) |  -  |
**502** | Upstream MKS-2 returned 5xx |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_customer_mks2_worker_nodes**
> Mks2WorkerNodeList list_customer_mks2_worker_nodes(fleet_id)

List MKS-2 worker nodes

Lists worker nodes in the fleet's MKS-2 cluster. Org-scoped: the caller's JWT org must own the fleet.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.mks2_worker_node_list import Mks2WorkerNodeList
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
    api_instance = vpcloud_client.KubernetesMKS2Api(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier

    try:
        # List MKS-2 worker nodes
        api_response = api_instance.list_customer_mks2_worker_nodes(fleet_id)
        print("The response of KubernetesMKS2Api->list_customer_mks2_worker_nodes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesMKS2Api->list_customer_mks2_worker_nodes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

[**Mks2WorkerNodeList**](Mks2WorkerNodeList.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns the worker-node list |  -  |
**400** | Fleet exists but is not MKS-2-backed, or upstream MKS-2 rejected the request as malformed |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org, or upstream MKS-2 has no cluster for the resolved id |  -  |
**500** | Internal failure before the upstream call (network unreachable, configuration, etc.) |  -  |
**502** | Upstream MKS-2 returned 5xx |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **uncordon_customer_mks2_worker_node**
> Mks2CordonNodeResponse uncordon_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key)

Uncordon an MKS-2 worker node

Marks the node schedulable again (reverses cordon), allowing the scheduler to place new pods on it. Org-scoped: the caller's JWT org must own the fleet. The node must be joined to the cluster; otherwise the request is rejected with 400. Idempotency: pass `Idempotency-Key` to make this safely retryable.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.mks2_cordon_node_response import Mks2CordonNodeResponse
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
    api_instance = vpcloud_client.KubernetesMKS2Api(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    node_id = 'node_id_example' # str | MKS-2 worker-node identifier (registry id)
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Body mismatch: Returns `422 Unprocessable Entity` (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.harbor.example.com/admin/fleets',             json=fleet_config,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key  # Same key for retries             }         )                  if response.status_code == 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code < 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception('Max retries exceeded') ```  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md (optional)

    try:
        # Uncordon an MKS-2 worker node
        api_response = api_instance.uncordon_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key)
        print("The response of KubernetesMKS2Api->uncordon_customer_mks2_worker_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesMKS2Api->uncordon_customer_mks2_worker_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| MKS-2 worker-node identifier (registry id) | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Body mismatch: Returns &#x60;422 Unprocessable Entity&#x60; (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.harbor.example.com/admin/fleets&#39;,             json&#x3D;fleet_config,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key  # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code &lt; 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60;  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md | [optional] 

### Return type

[**Mks2CordonNodeResponse**](Mks2CordonNodeResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Node uncordoned (marked schedulable) |  -  |
**400** | Fleet exists but is not MKS-2-backed, the node id is not a member of the fleet&#39;s bare-metal list, or upstream MKS-2 rejected the request (e.g. the node has not joined the cluster yet) |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org, or upstream MKS-2 has no cluster / no such node |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream MKS-2 returned 5xx |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

