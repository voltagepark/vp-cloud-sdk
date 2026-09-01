# Mks2WorkerNodeList

Worker-node list response. Mirrors mks2sdk.ListNodes200Response: `items` carries the page contents and `meta.nextCursor` carries the opaque continuation token for the next page (null when there are no more pages). The upstream service paginates; harbor is currently a passthrough and does not aggregate pages.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[Mks2WorkerNode]**](Mks2WorkerNode.md) | Worker nodes in the current page. Empty array (not null) when the cluster has no nodes registered. | [optional] 
**meta** | [**Mks2WorkerNodeListMeta**](Mks2WorkerNodeListMeta.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.mks2_worker_node_list import Mks2WorkerNodeList

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2WorkerNodeList from a JSON string
mks2_worker_node_list_instance = Mks2WorkerNodeList.from_json(json)
# print the JSON string representation of the object
print(Mks2WorkerNodeList.to_json())

# convert the object into a dict
mks2_worker_node_list_dict = mks2_worker_node_list_instance.to_dict()
# create an instance of Mks2WorkerNodeList from a dict
mks2_worker_node_list_from_dict = Mks2WorkerNodeList.from_dict(mks2_worker_node_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


