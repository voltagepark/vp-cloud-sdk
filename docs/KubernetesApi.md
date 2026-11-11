# vpcloud_client.KubernetesApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cordon_customer_mks2_worker_node**](KubernetesApi.md#cordon_customer_mks2_worker_node) | **POST** /v1/fleets/{fleetId}/kubernetes-v2/nodes/{nodeId}/cordon | Cordon a managed Kubernetes worker node
[**drain_customer_mks2_worker_node**](KubernetesApi.md#drain_customer_mks2_worker_node) | **POST** /v1/fleets/{fleetId}/kubernetes-v2/nodes/{nodeId}/drain | Drain a managed Kubernetes worker node
[**get_customer_mks2_cluster_health**](KubernetesApi.md#get_customer_mks2_cluster_health) | **GET** /v1/fleets/{fleetId}/kubernetes-v2/health | Get managed Kubernetes cluster health
[**get_customer_mks2_kubeconfig**](KubernetesApi.md#get_customer_mks2_kubeconfig) | **GET** /v1/fleets/{fleetId}/kubernetes-v2/kubeconfig | Download customer managed Kubernetes kubeconfig
[**get_customer_mks2_worker_node**](KubernetesApi.md#get_customer_mks2_worker_node) | **GET** /v1/fleets/{fleetId}/kubernetes-v2/nodes/{nodeId} | Get managed Kubernetes worker node detail
[**uncordon_customer_mks2_worker_node**](KubernetesApi.md#uncordon_customer_mks2_worker_node) | **POST** /v1/fleets/{fleetId}/kubernetes-v2/nodes/{nodeId}/uncordon | Uncordon a managed Kubernetes worker node


# **cordon_customer_mks2_worker_node**
> Mks2CordonNodeResponse cordon_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key)

Cordon a managed Kubernetes worker node

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
    api_instance = vpcloud_client.KubernetesApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    node_id = 'node_id_example' # str | Managed Kubernetes worker-node identifier (registry id)
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns `422 Unprocessable Entity` - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Key reuse: Returns `422 Unprocessable Entity` when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.sea1.voltagepark.com/v1/sshkeys',             json=ssh_key,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key # Same key for retries             }         )                  if response.status_code == 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception('Max retries exceeded') ``` (optional)

    try:
        # Cordon a managed Kubernetes worker node
        api_response = api_instance.cordon_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key)
        print("The response of KubernetesApi->cordon_customer_mks2_worker_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesApi->cordon_customer_mks2_worker_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| Managed Kubernetes worker-node identifier (registry id) | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns &#x60;422 Unprocessable Entity&#x60; - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Key reuse: Returns &#x60;422 Unprocessable Entity&#x60; when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.sea1.voltagepark.com/v1/sshkeys&#39;,             json&#x3D;ssh_key,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60; | [optional] 

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
**400** | Fleet exists but is not Kubernetes-backed, the node id is not a member of the fleet&#39;s bare-metal list, or the Kubernetes control plane rejected the request (e.g. the node has not joined the cluster yet) |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org, or the Kubernetes control plane has no cluster / no such node |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | The Kubernetes control plane returned 5xx |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **drain_customer_mks2_worker_node**
> Mks2DrainNodeResponse drain_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key, mks2_drain_node_request=mks2_drain_node_request)

Drain a managed Kubernetes worker node

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
    api_instance = vpcloud_client.KubernetesApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    node_id = 'node_id_example' # str | Managed Kubernetes worker-node identifier (registry id)
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns `422 Unprocessable Entity` - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Key reuse: Returns `422 Unprocessable Entity` when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.sea1.voltagepark.com/v1/sshkeys',             json=ssh_key,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key # Same key for retries             }         )                  if response.status_code == 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception('Max retries exceeded') ``` (optional)
    mks2_drain_node_request = vpcloud_client.Mks2DrainNodeRequest() # Mks2DrainNodeRequest |  (optional)

    try:
        # Drain a managed Kubernetes worker node
        api_response = api_instance.drain_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key, mks2_drain_node_request=mks2_drain_node_request)
        print("The response of KubernetesApi->drain_customer_mks2_worker_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesApi->drain_customer_mks2_worker_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| Managed Kubernetes worker-node identifier (registry id) | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns &#x60;422 Unprocessable Entity&#x60; - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Key reuse: Returns &#x60;422 Unprocessable Entity&#x60; when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.sea1.voltagepark.com/v1/sshkeys&#39;,             json&#x3D;ssh_key,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60; | [optional] 
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

# **get_customer_mks2_cluster_health**
> Mks2ClusterHealth get_customer_mks2_cluster_health(fleet_id)

Get managed Kubernetes cluster health

Returns the current health status of the managed Kubernetes cluster bound to the fleet: top-level health, control-plane component health, per-worker-node health, networking (Cilium) health, and API-server-to-worker connectivity status. Org-scoped: the caller's JWT org must own the fleet. Reads are live (not cached). Returns 404 when the cluster has no health snapshot yet, 502 when the health service reports a server error, and 500 when the health service cannot be reached.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.mks2_cluster_health import Mks2ClusterHealth
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
    api_instance = vpcloud_client.KubernetesApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier

    try:
        # Get managed Kubernetes cluster health
        api_response = api_instance.get_customer_mks2_cluster_health(fleet_id)
        print("The response of KubernetesApi->get_customer_mks2_cluster_health:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesApi->get_customer_mks2_cluster_health: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

[**Mks2ClusterHealth**](Mks2ClusterHealth.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns cluster health |  -  |
**400** | Fleet exists but is not Kubernetes-backed, or the Kubernetes control plane rejected the request as malformed |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org, or the Kubernetes control plane has no health snapshot for the cluster yet |  -  |
**500** | Internal failure before the upstream call (network unreachable, configuration, etc.) |  -  |
**502** | The Kubernetes control plane returned 5xx |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_mks2_kubeconfig**
> KubeconfigV2Response get_customer_mks2_kubeconfig(fleet_id)

Download customer managed Kubernetes kubeconfig

Returns a customer-role kubeconfig for the managed Kubernetes cluster bound to the fleet. The credential is time-limited; clients should refetch before expiresAt. Org-scoped: the caller's JWT org must own the fleet.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.kubeconfig_v2_response import KubeconfigV2Response
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
    api_instance = vpcloud_client.KubernetesApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier

    try:
        # Download customer managed Kubernetes kubeconfig
        api_response = api_instance.get_customer_mks2_kubeconfig(fleet_id)
        print("The response of KubernetesApi->get_customer_mks2_kubeconfig:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesApi->get_customer_mks2_kubeconfig: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

[**KubeconfigV2Response**](KubeconfigV2Response.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns a customer-role kubeconfig |  -  |
**400** | Fleet exists but is not Kubernetes-backed |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org |  -  |
**500** | The Kubernetes control plane error or internal failure |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_mks2_worker_node**
> Mks2WorkerNodeDetail get_customer_mks2_worker_node(fleet_id, node_id)

Get managed Kubernetes worker node detail

Returns the full detail for a single worker node in the fleet's managed Kubernetes cluster, including Kubernetes conditions, GPU info, labels/annotations, and registration timestamps. Org-scoped: the caller's JWT org must own the fleet. Unlike the list endpoint (joined-only), this resolves registered-but-not-yet-joined nodes by id.

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
    api_instance = vpcloud_client.KubernetesApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    node_id = 'node_id_example' # str | Managed Kubernetes worker-node identifier (registry id)

    try:
        # Get managed Kubernetes worker node detail
        api_response = api_instance.get_customer_mks2_worker_node(fleet_id, node_id)
        print("The response of KubernetesApi->get_customer_mks2_worker_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesApi->get_customer_mks2_worker_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| Managed Kubernetes worker-node identifier (registry id) | 

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
**400** | Fleet exists but is not Kubernetes-backed, or the Kubernetes control plane rejected the request as malformed |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org, or the Kubernetes control plane has no cluster / no such node |  -  |
**500** | Internal failure before the upstream call (network unreachable, configuration, etc.) |  -  |
**502** | The Kubernetes control plane returned 5xx |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **uncordon_customer_mks2_worker_node**
> Mks2CordonNodeResponse uncordon_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key)

Uncordon a managed Kubernetes worker node

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
    api_instance = vpcloud_client.KubernetesApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    node_id = 'node_id_example' # str | Managed Kubernetes worker-node identifier (registry id)
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns `422 Unprocessable Entity` - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Key reuse: Returns `422 Unprocessable Entity` when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.sea1.voltagepark.com/v1/sshkeys',             json=ssh_key,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key # Same key for retries             }         )                  if response.status_code == 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception('Max retries exceeded') ``` (optional)

    try:
        # Uncordon a managed Kubernetes worker node
        api_response = api_instance.uncordon_customer_mks2_worker_node(fleet_id, node_id, idempotency_key=idempotency_key)
        print("The response of KubernetesApi->uncordon_customer_mks2_worker_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KubernetesApi->uncordon_customer_mks2_worker_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **node_id** | **str**| Managed Kubernetes worker-node identifier (registry id) | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns &#x60;422 Unprocessable Entity&#x60; - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Key reuse: Returns &#x60;422 Unprocessable Entity&#x60; when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.sea1.voltagepark.com/v1/sshkeys&#39;,             json&#x3D;ssh_key,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60; | [optional] 

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
**400** | Fleet exists but is not Kubernetes-backed, the node id is not a member of the fleet&#39;s bare-metal list, or the Kubernetes control plane rejected the request (e.g. the node has not joined the cluster yet) |  -  |
**401** | Missing or invalid authentication |  -  |
**404** | Fleet not found in caller&#39;s org, or the Kubernetes control plane has no cluster / no such node |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | The Kubernetes control plane returned 5xx |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

