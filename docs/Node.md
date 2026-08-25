# Node

A node represents an individual compute instance within a fleet

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_name** | **str** | Unique identifier for the node | 
**state** | [**NodeState**](NodeState.md) |  | 
**public_ip** | **str** | Public IP address of the node | 
**fleet_id** | **str** | Fleet ID associated with the node, if any | [optional] 
**gpu_type** | **str** | GPU model installed on this node. Not an enum: new hardware models must reach clients rather than break deserialization. Absent when the model is not known. | [optional] 

## Example

```python
from vpcloud_client.models.node import Node

# TODO update the JSON string below
json = "{}"
# create an instance of Node from a JSON string
node_instance = Node.from_json(json)
# print the JSON string representation of the object
print(Node.to_json())

# convert the object into a dict
node_dict = node_instance.to_dict()
# create an instance of Node from a dict
node_from_dict = Node.from_dict(node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


