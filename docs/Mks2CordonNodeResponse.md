# Mks2CordonNodeResponse

Result of a cordon or uncordon operation. `schedulable` reflects the node's scheduling state after the operation (false after cordon, true after uncordon).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** | MKS-2 worker-node identifier (registry id) the operation targeted. | 
**schedulable** | **bool** | Whether pods can be scheduled on the node after the operation. false after cordon, true after uncordon. | 
**message** | **str** | Human-readable status message describing the result, when available. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_cordon_node_response import Mks2CordonNodeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2CordonNodeResponse from a JSON string
mks2_cordon_node_response_instance = Mks2CordonNodeResponse.from_json(json)
# print the JSON string representation of the object
print(Mks2CordonNodeResponse.to_json())

# convert the object into a dict
mks2_cordon_node_response_dict = mks2_cordon_node_response_instance.to_dict()
# create an instance of Mks2CordonNodeResponse from a dict
mks2_cordon_node_response_from_dict = Mks2CordonNodeResponse.from_dict(mks2_cordon_node_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


