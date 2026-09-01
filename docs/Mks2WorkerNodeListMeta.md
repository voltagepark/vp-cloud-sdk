# Mks2WorkerNodeListMeta

Pagination metadata for worker-node list responses. Mirrors mks2sdk.ListMeta.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_cursor** | **str** | Opaque cursor for the next page (null when there are no more pages). | [optional] 

## Example

```python
from vpcloud_client.models.mks2_worker_node_list_meta import Mks2WorkerNodeListMeta

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2WorkerNodeListMeta from a JSON string
mks2_worker_node_list_meta_instance = Mks2WorkerNodeListMeta.from_json(json)
# print the JSON string representation of the object
print(Mks2WorkerNodeListMeta.to_json())

# convert the object into a dict
mks2_worker_node_list_meta_dict = mks2_worker_node_list_meta_instance.to_dict()
# create an instance of Mks2WorkerNodeListMeta from a dict
mks2_worker_node_list_meta_from_dict = Mks2WorkerNodeListMeta.from_dict(mks2_worker_node_list_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


