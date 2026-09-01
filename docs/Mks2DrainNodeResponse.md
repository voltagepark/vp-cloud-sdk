# Mks2DrainNodeResponse

Result of a node drain. `evicted` and `failed` are included when reported.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** | MKS-2 worker-node identifier (registry id) the drain targeted. | 
**evicted** | **int** | Number of pods evicted from the node, when reported. | [optional] 
**failed** | **List[str]** | Identifiers of pods that could not be evicted, when reported. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_drain_node_response import Mks2DrainNodeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2DrainNodeResponse from a JSON string
mks2_drain_node_response_instance = Mks2DrainNodeResponse.from_json(json)
# print the JSON string representation of the object
print(Mks2DrainNodeResponse.to_json())

# convert the object into a dict
mks2_drain_node_response_dict = mks2_drain_node_response_instance.to_dict()
# create an instance of Mks2DrainNodeResponse from a dict
mks2_drain_node_response_from_dict = Mks2DrainNodeResponse.from_dict(mks2_drain_node_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


