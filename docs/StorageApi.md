# vpcloud_client.StorageApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_storage_view**](StorageApi.md#add_storage_view) | **POST** /v1/fleets/{fleetId}/storage/views | Add a VAST storage view
[**delete_storage_view**](StorageApi.md#delete_storage_view) | **DELETE** /v1/fleets/{fleetId}/storage/views/{view} | Delete a VAST storage view
[**get_storage_view**](StorageApi.md#get_storage_view) | **GET** /v1/fleets/{fleetId}/storage/views/{view} | Get a VAST storage view
[**list_storage_views**](StorageApi.md#list_storage_views) | **GET** /v1/fleets/{fleetId}/storage/views | List VAST storage views
[**update_storage_view**](StorageApi.md#update_storage_view) | **PATCH** /v1/fleets/{fleetId}/storage/views/{view} | Update a VAST storage view


# **add_storage_view**
> StorageView add_storage_view(fleet_id, add_storage_view_request, idempotency_key=idempotency_key)

Add a VAST storage view

Adds a new physical VAST storage view (mount point with size/quota) to the fleet's reservation, optionally triggering VAST provisioning. Org-scoped: the caller's JWT org must own the fleet. Returns 202 with the freshly-added view carrying `state: "provisioning"`; callers should poll `GET /v1/fleets/{fleetId}/storage/views/{view}` until `state == "active"` to confirm provisioning completion.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.add_storage_view_request import AddStorageViewRequest
from vpcloud_client.models.storage_view import StorageView
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
    api_instance = vpcloud_client.StorageApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    add_storage_view_request = vpcloud_client.AddStorageViewRequest() # AddStorageViewRequest | 
    idempotency_key = '123e4567-e89b-12d3-a456-426614174000' # str | **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** ```javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey = crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey = uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey = `${userId}-${timestamp}-${nonce}`; const idempotencyKey = `order-${orderId}`; // If order ID is unique ```  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns `409 Conflict` (retry after 5 seconds) - Body mismatch: Returns `422 Unprocessable Entity` (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** ```python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries=3):     # Generate key once for this operation     idempotency_key = str(uuid.uuid4())          for attempt in range(max_retries):         response = requests.post(             'https://api.harbor.example.com/admin/fleets',             json=fleet_config,             headers={                 'Authorization': f'Bearer {token}',                 'Idempotency-Key': idempotency_key  # Same key for retries             }         )                  if response.status_code == 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code < 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception('Max retries exceeded') ```  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md (optional)

    try:
        # Add a VAST storage view
        api_response = api_instance.add_storage_view(fleet_id, add_storage_view_request, idempotency_key=idempotency_key)
        print("The response of StorageApi->add_storage_view:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StorageApi->add_storage_view: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **add_storage_view_request** | [**AddStorageViewRequest**](AddStorageViewRequest.md)|  | 
 **idempotency_key** | **str**| **Idempotency Key for Safe Request Retries**  Optional but **strongly recommended** for all mutation operations (POST, PUT, PATCH, DELETE) to enable safe request retries.  **How It Works:** - Provide a unique key when making a request - If the request succeeds, the response is cached for 24 hours - Retrying with the same key returns the cached response immediately - Prevents duplicate operations (e.g., creating multiple fleets for one request)  **Key Requirements:** - **You are responsible for ensuring uniqueness** across your requests - Maximum length: 255 characters - Any string format is accepted (UUID v4, ULID, custom identifiers, etc.) - Recommended: Use UUID v4 for guaranteed global uniqueness  **Key Generation (Recommended):** &#x60;&#x60;&#x60;javascript // UUID v4 - Recommended for guaranteed uniqueness const idempotencyKey &#x3D; crypto.randomUUID(); // Browser/Node.js 19+ // OR const idempotencyKey &#x3D; uuidv4(); // using uuid library  // Alternative: Use your own unique identifier const idempotencyKey &#x3D; &#x60;${userId}-${timestamp}-${nonce}&#x60;; const idempotencyKey &#x3D; &#x60;order-${orderId}&#x60;; // If order ID is unique &#x60;&#x60;&#x60;  **Retry Guidelines:** - **Network timeout/failure**: Retry with the **SAME key** to get cached result - **409 Conflict** (concurrent request): Wait 5 seconds, retry with **SAME key** - **422 Unprocessable Entity** (body mismatch): Use a **NEW key** or fix request body - **500 Internal Server Error**: Retry with **SAME key** (or NEW key to force fresh attempt)  **Response Behavior:** - First request: Processes normally, caches response for 24 hours - Duplicate requests: Returns cached response with original status code - Requests in-progress: Returns &#x60;409 Conflict&#x60; (retry after 5 seconds) - Body mismatch: Returns &#x60;422 Unprocessable Entity&#x60; (key reused with different data)  **TTL (Time-To-Live):** - In-progress requests: 5 minutes (crash recovery) - Completed/failed requests: 24 hours (response caching) - Keys automatically expire and can be reused after TTL  **Best Practices:** 1. Generate key client-side before making the request 2. Store the key with your request context for retries 3. Use a new key for each distinct operation (not per retry) 4. Use UUID v4 format for guaranteed uniqueness 5. Maximum length: 255 characters  **Example Usage:** &#x60;&#x60;&#x60;python import uuid import requests  def create_fleet_with_retry(fleet_config, max_retries&#x3D;3):     # Generate key once for this operation     idempotency_key &#x3D; str(uuid.uuid4())          for attempt in range(max_retries):         response &#x3D; requests.post(             &#39;https://api.harbor.example.com/admin/fleets&#39;,             json&#x3D;fleet_config,             headers&#x3D;{                 &#39;Authorization&#39;: f&#39;Bearer {token}&#39;,                 &#39;Idempotency-Key&#39;: idempotency_key  # Same key for retries             }         )                  if response.status_code &#x3D;&#x3D; 409:  # Concurrent request             time.sleep(5)  # Wait and retry             continue         elif response.status_code &lt; 500:             return response  # Success or client error         # else: retry on 500 errors          raise Exception(&#39;Max retries exceeded&#39;) &#x60;&#x60;&#x60;  See full documentation at: https://github.com/voltagepark/harbor-service/blob/main/docs/IDEMPOTENCY.md | [optional] 

### Return type

[**StorageView**](StorageView.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Storage view add accepted. |  -  |
**400** | Malformed reservation identifier or invalid request body |  -  |
**401** | Missing or invalid JWT |  -  |
**404** | Fleet not found (or not owned by the caller&#39;s org) |  -  |
**409** | A storage view with this mount point already exists |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream Thundercat returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_storage_view**
> delete_storage_view(fleet_id, view)

Delete a VAST storage view

Deletes a single physical VAST storage view by mount point. Org-scoped: the caller's JWT org must own the fleet.

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
    api_instance = vpcloud_client.StorageApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    view = 'view_example' # str | Storage view identifier (mount point, without a leading slash).

    try:
        # Delete a VAST storage view
        api_instance.delete_storage_view(fleet_id, view)
    except Exception as e:
        print("Exception when calling StorageApi->delete_storage_view: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **view** | **str**| Storage view identifier (mount point, without a leading slash). | 

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
**204** | Storage view deleted. |  -  |
**400** | Malformed reservation identifier or invalid view path segment |  -  |
**401** | Missing or invalid JWT |  -  |
**404** | Fleet not found (or not owned by the caller&#39;s org), or storage view not found |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream Thundercat returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_storage_view**
> StorageView get_storage_view(fleet_id, view)

Get a VAST storage view

Returns a single physical VAST storage view by mount point. Org-scoped: the caller's JWT org must own the fleet. The `state` field on the response is the source of truth for provisioning progress; poll this endpoint after a 202 from add/update until `state == "active"` (or `unhealthy` to fail fast).

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.storage_view import StorageView
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
    api_instance = vpcloud_client.StorageApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    view = 'view_example' # str | Storage view identifier (mount point, without a leading slash).

    try:
        # Get a VAST storage view
        api_response = api_instance.get_storage_view(fleet_id, view)
        print("The response of StorageApi->get_storage_view:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StorageApi->get_storage_view: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **view** | **str**| Storage view identifier (mount point, without a leading slash). | 

### Return type

[**StorageView**](StorageView.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The storage view. |  -  |
**400** | Malformed reservation identifier or invalid view path segment |  -  |
**401** | Missing or invalid JWT |  -  |
**404** | Fleet not found (or not owned by the caller&#39;s org), or storage view not found |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream Thundercat returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_storage_views**
> StorageViewListResponse list_storage_views(fleet_id)

List VAST storage views

Lists the physical VAST storage views (mount points and their quotas) provisioned for the fleet's reservation. Org-scoped: the caller's JWT org must own the fleet. Each returned view carries a `state` field; use it to confirm provisioning completion (poll until `state == "active"`). If the fleet exists but storage has not been materialized yet, returns 200 with `items: []` and `storagePending: true`.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.storage_view_list_response import StorageViewListResponse
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
    api_instance = vpcloud_client.StorageApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier

    try:
        # List VAST storage views
        api_response = api_instance.list_storage_views(fleet_id)
        print("The response of StorageApi->list_storage_views:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StorageApi->list_storage_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

[**StorageViewListResponse**](StorageViewListResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Storage views for the fleet&#39;s reservation. When the fleet exists but storage has not been materialized yet, &#x60;items&#x60; is empty and &#x60;storagePending&#x60; is true. |  -  |
**400** | Fleet&#39;s stored reservation identifier is malformed |  -  |
**401** | Missing or invalid JWT |  -  |
**404** | Fleet not found (or not owned by the caller&#39;s org) |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream Thundercat returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_storage_view**
> StorageView update_storage_view(fleet_id, view, update_storage_view_request)

Update a VAST storage view

Updates the size/quota of a single physical VAST storage view by mount point. Org-scoped: the caller's JWT org must own the fleet. Returns 202 with the post-update view state.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.storage_view import StorageView
from vpcloud_client.models.update_storage_view_request import UpdateStorageViewRequest
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
    api_instance = vpcloud_client.StorageApi(api_client)
    fleet_id = 'fleet_id_example' # str | Fleet identifier
    view = 'view_example' # str | Storage view identifier (mount point, without a leading slash).
    update_storage_view_request = vpcloud_client.UpdateStorageViewRequest() # UpdateStorageViewRequest | 

    try:
        # Update a VAST storage view
        api_response = api_instance.update_storage_view(fleet_id, view, update_storage_view_request)
        print("The response of StorageApi->update_storage_view:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StorageApi->update_storage_view: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 
 **view** | **str**| Storage view identifier (mount point, without a leading slash). | 
 **update_storage_view_request** | [**UpdateStorageViewRequest**](UpdateStorageViewRequest.md)|  | 

### Return type

[**StorageView**](StorageView.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Storage view update accepted. |  -  |
**400** | Malformed reservation identifier, invalid view path segment, or invalid request body |  -  |
**401** | Missing or invalid JWT |  -  |
**404** | Fleet not found (or not owned by the caller&#39;s org), or storage view not found |  -  |
**500** | Internal failure before the upstream call |  -  |
**502** | Upstream Thundercat returned an error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

