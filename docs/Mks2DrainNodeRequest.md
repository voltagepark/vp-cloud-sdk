# Mks2DrainNodeRequest

Optional tuning for a node drain. Every field is optional; omit the body (or any field) to use the defaults below. These defaults are owned and applied by Harbor, so an omitted, empty ({}), or partial body all behave identically.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**grace_period_seconds** | **int** | Grace period (seconds) granted to evicted pods before they are forcibly terminated. Maps to the eviction grace period. | [optional] [default to 30]
**delete_local_data** | **bool** | Whether to evict pods backed by emptyDir / local storage (their data is lost). Not currently honored; accepted for forward compatibility and has no effect yet. | [optional] [default to False]
**ignore_daemon_sets** | **bool** | Whether to proceed with the drain even though DaemonSet-managed pods cannot be evicted (they are skipped). | [optional] [default to True]

## Example

```python
from vpcloud_client.models.mks2_drain_node_request import Mks2DrainNodeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2DrainNodeRequest from a JSON string
mks2_drain_node_request_instance = Mks2DrainNodeRequest.from_json(json)
# print the JSON string representation of the object
print(Mks2DrainNodeRequest.to_json())

# convert the object into a dict
mks2_drain_node_request_dict = mks2_drain_node_request_instance.to_dict()
# create an instance of Mks2DrainNodeRequest from a dict
mks2_drain_node_request_from_dict = Mks2DrainNodeRequest.from_dict(mks2_drain_node_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


