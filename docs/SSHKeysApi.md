# vpcloud_client.SSHKeysApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_fleet_ssh_key**](SSHKeysApi.md#add_fleet_ssh_key) | **POST** /v1/fleets/{fleetId}/sshkeys | Apply an SSH key to a running fleet
[**create_ssh_key**](SSHKeysApi.md#create_ssh_key) | **POST** /v1/sshkeys | Add an SSH key
[**delete_ssh_key**](SSHKeysApi.md#delete_ssh_key) | **DELETE** /v1/sshkeys/{sshKeyId} | Remove an SSH key
[**list_ssh_keys**](SSHKeysApi.md#list_ssh_keys) | **GET** /v1/sshkeys | List your SSH keys
[**remove_fleet_ssh_key**](SSHKeysApi.md#remove_fleet_ssh_key) | **DELETE** /v1/fleets/{fleetId}/sshkeys/{sshKeyId} | Revoke an SSH key from a running fleet


# **add_fleet_ssh_key**
> AddFleetSSHKeyResponse add_fleet_ssh_key(fleet_id, add_fleet_ssh_key_request, idempotency_key=idempotency_key)

Apply an SSH key to a running fleet

Applies an SSH key already registered in the organization to a fleet that is already running, so its nodes accept the key without being rebuilt. Org-scoped: the caller's JWT org must own both the fleet and the key.

Keys are only added. A key already on a node is left alone, and keys on a node that are not in the request are never removed — this endpoint cannot revoke access. Re-submitting the same key is safe and is the way to repair a fleet where an earlier attempt reached only some nodes.

Returns 202 once the infrastructure service has accepted the work; the keys are written to nodes asynchronously. There is no status endpoint in this iteration — confirm by logging in. Only nodes that are already provisioned are visited; nodes added later pick the key up from the reservation's cloud-init.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.add_fleet_ssh_key_request import AddFleetSSHKeyRequest
from vpcloud_client.models.add_fleet_ssh_key_response import AddFleetSSHKeyResponse
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
    api_instance = vpcloud_client.SSHKeysApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    add_fleet_ssh_key_request = vpcloud_client.AddFleetSSHKeyRequest() # AddFleetSSHKeyRequest | 
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns `422 Unprocessable Entity` - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Key reuse: Returns `422 Unprocessable Entity` when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.sea1.voltagepark.com/v1/sshkeys',             json=ssh_key,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key # Same key for retries             }         )                  if response.status_code == 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception('Max retries exceeded') ``` (optional)

    try:
        # Apply an SSH key to a running fleet
        api_response = api_instance.add_fleet_ssh_key(fleet_id, add_fleet_ssh_key_request, idempotency_key=idempotency_key)
        print("The response of SSHKeysApi->add_fleet_ssh_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SSHKeysApi->add_fleet_ssh_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **add_fleet_ssh_key_request** | [**AddFleetSSHKeyRequest**](AddFleetSSHKeyRequest.md)|  | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns &#x60;422 Unprocessable Entity&#x60; - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Key reuse: Returns &#x60;422 Unprocessable Entity&#x60; when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.sea1.voltagepark.com/v1/sshkeys&#39;,             json&#x3D;ssh_key,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60; | [optional] 

### Return type

[**AddFleetSSHKeyResponse**](AddFleetSSHKeyResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Key propagation accepted. Nodes are updated asynchronously. |  -  |
**400** | Invalid fleet identifier or request body |  -  |
**401** | Missing or invalid JWT |  -  |
**403** | Caller does not have the Administrator role |  -  |
**404** | Fleet or SSH key not found (or not owned by the caller&#39;s org) |  -  |
**409** | Fleet is not in a state that accepts key propagation |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream infrastructure returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_ssh_key**
> SSHKey create_ssh_key(create_ssh_key_request, idempotency_key=idempotency_key)

Add an SSH key

Register your SSH public key for secure access to fleet nodes. Once added, this key will be automatically installed on all new nodes in your fleets.

**When to use:**
- First time setup - add your SSH key before creating fleets
- Team member needs access - add their public key
- Rotate keys - add new key before removing old one

**Supported formats:** OpenSSH, RFC4716, PKCS8, PKCS1 (automatically normalized to OpenSSH)

**Idempotent:** Use `Idempotency-Key` header to safely retry if your request times out.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.create_ssh_key_request import CreateSSHKeyRequest
from vpcloud_client.models.ssh_key import SSHKey
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
    api_instance = vpcloud_client.SSHKeysApi(api_client)
    create_ssh_key_request = {"username":"john_doe","publicKey":"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl user@example.com","description":"Work laptop"} # CreateSSHKeyRequest | 
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns `422 Unprocessable Entity` - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Key reuse: Returns `422 Unprocessable Entity` when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.sea1.voltagepark.com/v1/sshkeys',             json=ssh_key,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key # Same key for retries             }         )                  if response.status_code == 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception('Max retries exceeded') ``` (optional)

    try:
        # Add an SSH key
        api_response = api_instance.create_ssh_key(create_ssh_key_request, idempotency_key=idempotency_key)
        print("The response of SSHKeysApi->create_ssh_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SSHKeysApi->create_ssh_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_ssh_key_request** | [**CreateSSHKeyRequest**](CreateSSHKeyRequest.md)|  | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns &#x60;422 Unprocessable Entity&#x60; - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Key reuse: Returns &#x60;422 Unprocessable Entity&#x60; when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.sea1.voltagepark.com/v1/sshkeys&#39;,             json&#x3D;ssh_key,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60; | [optional] 

### Return type

[**SSHKey**](SSHKey.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | SSH key appended to an existing user record. Returned when the request&#39;s &#x60;username&#x60; already has an SSH-key record for the caller&#39;s organization; the new public key is appended to that record and the full updated SSH key is returned. |  -  |
**201** | New SSH-key record created. Returned when the request&#39;s &#x60;username&#x60; had no SSH-key record yet for the caller&#39;s organization. |  -  |
**400** | Bad request - invalid SSH key format or validation failed |  -  |
**401** | Unauthorized |  -  |
**409** | Conflict - duplicate key name or fingerprint |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_ssh_key**
> delete_ssh_key(ssh_key_id, idempotency_key=idempotency_key)

Remove an SSH key

Remove an SSH key from your organization. The key will no longer be installed on new fleet nodes.

**When to use:**
- Revoke access when a team member leaves
- Remove compromised keys
- Clean up unused keys

**Important:** Existing nodes keep the key until they're replaced. This operation is idempotent - safe to call multiple times.

**Fleets:** If the user's keys were applied to running fleets, they are taken off those fleets' nodes first. If a fleet can't be reached, the user is kept and the response is 502 with `details.fleetIds`, but the fleets that were reached are already updated; retry to finish.

**Slurm:** Slurm cluster users are separate from SSH keys. Deleting an SSH key does not change any Slurm cluster.

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
    api_instance = vpcloud_client.SSHKeysApi(api_client)
    ssh_key_id = '550e8400-e29b-41d4-a716-446655440000' # str | SSH key identifier (from list SSH keys response)
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns `422 Unprocessable Entity` - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Key reuse: Returns `422 Unprocessable Entity` when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.sea1.voltagepark.com/v1/sshkeys',             json=ssh_key,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key # Same key for retries             }         )                  if response.status_code == 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception('Max retries exceeded') ``` (optional)

    try:
        # Remove an SSH key
        api_instance.delete_ssh_key(ssh_key_id, idempotency_key=idempotency_key)
    except Exception as e:
        print("Exception when calling SSHKeysApi->delete_ssh_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ssh_key_id** | **str**| SSH key identifier (from list SSH keys response) | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns &#x60;422 Unprocessable Entity&#x60; - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Key reuse: Returns &#x60;422 Unprocessable Entity&#x60; when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.sea1.voltagepark.com/v1/sshkeys&#39;,             json&#x3D;ssh_key,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60; | [optional] 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | SSH key deleted successfully |  -  |
**401** | Unauthorized |  -  |
**404** | SSH key not found |  -  |
**500** | Internal server error |  -  |
**502** | The user&#39;s keys are still on one or more fleets (listed in details.fleetIds), so it was not deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_ssh_keys**
> List[SSHKey] list_ssh_keys()

List your SSH keys

Get all SSH keys registered for your organization. These keys are automatically installed on fleet nodes for secure access.

**When to use:**
- Show available SSH keys in your UI
- Verify which keys are registered
- Check key fingerprints before adding duplicates

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.ssh_key import SSHKey
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
    api_instance = vpcloud_client.SSHKeysApi(api_client)

    try:
        # List your SSH keys
        api_response = api_instance.list_ssh_keys()
        print("The response of SSHKeysApi->list_ssh_keys:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SSHKeysApi->list_ssh_keys: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[SSHKey]**](SSHKey.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns array of SSH keys |  -  |
**401** | Unauthorized |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_fleet_ssh_key**
> RemoveFleetSSHKeyResponse remove_fleet_ssh_key(fleet_id, ssh_key_id, idempotency_key=idempotency_key)

Revoke an SSH key from a running fleet

Removes every public key held by an SSH key record from a fleet's running nodes, so those nodes stop accepting them. Org-scoped: the caller's JWT org must own both the fleet and the key.

The fleet is named explicitly, and only that fleet is touched. Other fleets holding the same key keep it, and a node that never had the user is left alone rather than having the account created for it.

The passwordless sudo rule the infrastructure service granted the user on this fleet is removed along with the keys. Sudo from any other source — the fleet's cloud-init, or membership of the sudo group — is not touched.

The key stays registered in the organization and can be applied again later. To delete the record itself, use DELETE /v1/sshkeys/{sshKeyId}.

Returns 202 once the infrastructure service has accepted the work; the nodes are updated asynchronously. There is no status endpoint in this iteration — confirm by attempting to log in. Re-submitting is safe.

Nodes added to the fleet after this call can still pick the key up from the reservation's cloud-init, which this endpoint does not rewrite.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.remove_fleet_ssh_key_response import RemoveFleetSSHKeyResponse
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
    api_instance = vpcloud_client.SSHKeysApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    ssh_key_id = 'ssh_key_id_example' # str | Identifier of an SSH key record in the caller's organization. Every public key held by that record is removed from the fleet.
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns `422 Unprocessable Entity` - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Key reuse: Returns `422 Unprocessable Entity` when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.sea1.voltagepark.com/v1/sshkeys',             json=ssh_key,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key # Same key for retries             }         )                  if response.status_code == 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception('Max retries exceeded') ``` (optional)

    try:
        # Revoke an SSH key from a running fleet
        api_response = api_instance.remove_fleet_ssh_key(fleet_id, ssh_key_id, idempotency_key=idempotency_key)
        print("The response of SSHKeysApi->remove_fleet_ssh_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SSHKeysApi->remove_fleet_ssh_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **ssh_key_id** | **str**| Identifier of an SSH key record in the caller&#39;s organization. Every public key held by that record is removed from the fleet. | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - The response is cached for 24 hours, including error responses, except a 5xx from a DELETE or PUT (see TTL below) - Retrying with the same key returns the cached response immediately; after an uncached DELETE or PUT 5xx, the request runs again - Prevents duplicate operations (e.g., creating the same resource twice for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - A key is bound to the organization and to the method and path of the request that first used it; reusing it from another organization or for a different method or path returns &#x60;422 Unprocessable Entity&#x60; - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (key already used with a different body, method, path, or organization): Use a **NEW key**, or resend the original request unchanged - **5xx Server Error**: For DELETE and PUT, retrying with the **SAME key** runs the request again. For POST and PATCH, the same key returns the cached error; use a **NEW key** to force a fresh attempt  **Response Behavior:** - First request: Processes normally, caches response for 24 hours (except a DELETE or PUT 5xx) - Duplicate requests: Returns cached response with original status code; after an uncached DELETE or PUT 5xx, processes the request again - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Key reuse: Returns &#x60;422 Unprocessable Entity&#x60; when the key was first used with a different body, method, path, or organization  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching; a 5xx from DELETE or PUT releases the key instead, unless the release itself fails) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import time import uuid import requests  def create_ssh_key_with_retry(ssh_key, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.sea1.voltagepark.com/v1/sshkeys&#39;,             json&#x3D;ssh_key,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409: # Concurrent request             time.sleep(5) # Wait and retry             continue         return response # A POST 5xx is cached for this key; check state before retrying with a new key          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60; | [optional] 

### Return type

[**RemoveFleetSSHKeyResponse**](RemoveFleetSSHKeyResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Key revocation accepted. Nodes are updated asynchronously. |  -  |
**400** | Invalid fleet or SSH key identifier |  -  |
**401** | Missing or invalid JWT |  -  |
**403** | Caller does not have the Administrator role |  -  |
**404** | Fleet or SSH key not found (or not owned by the caller&#39;s org) |  -  |
**409** | Fleet is not in a state that accepts key changes |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream infrastructure returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

