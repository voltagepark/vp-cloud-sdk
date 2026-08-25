# StorageView

Harbor's typed view of a single physical VAST storage view (a mount point and its quotas). Sizes are in bytes; Thundercat's unit/wire format is not exposed to callers.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mount_point** | **str** | Mount point for the storage view (e.g., &#39;/data&#39;, &#39;/home&#39;). | 
**size** | **int** | Provisioned size in bytes. | [optional] 
**soft_limit** | **int** | Soft quota in bytes, when set. | [optional] 
**hard_limit** | **int** | Hard quota in bytes, when set. | [optional] 
**state** | **str** | Lifecycle state of the storage view on the backing VAST tenant. Callers should treat &#x60;active&#x60; as the only \&quot;ready to use\&quot; state; &#x60;provisioning&#x60; and &#x60;modifying&#x60; are transient and callers that just issued a 202 add/update should poll &#x60;GET .../storage/views/{view}&#x60; until &#x60;state &#x3D;&#x3D; \&quot;active\&quot;&#x60; (or &#x60;unhealthy&#x60; to fail fast). The &#x60;terminating&#x60; state is observable when a delete is in progress or during fleet teardown. The field is optional and will be **absent** from the response for three reasons: (1) the upstream Thundercat response omitted it (older deployments); (2) Thundercat returned a lifecycle value Harbor does not recognize (forward-compatibility with future upstream enum members — the raw value is captured in Harbor logs); (3) the PATCH refresh-GET failed and Harbor fell back to a synthesized response body. In all three cases callers should treat an absent &#x60;state&#x60; as \&quot;unknown, please re-GET\&quot;. Additional caveat: on a POST 202 response served via idempotency-key replay, &#x60;state&#x60; reflects the original request&#39;s timepoint (typically &#x60;provisioning&#x60;), not the current lifecycle state; re-&#x60;GET&#x60; to obtain authoritative state. | [optional] 

## Example

```python
from vpcloud_client.models.storage_view import StorageView

# TODO update the JSON string below
json = "{}"
# create an instance of StorageView from a JSON string
storage_view_instance = StorageView.from_json(json)
# print the JSON string representation of the object
print(StorageView.to_json())

# convert the object into a dict
storage_view_dict = storage_view_instance.to_dict()
# create an instance of StorageView from a dict
storage_view_from_dict = StorageView.from_dict(storage_view_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


