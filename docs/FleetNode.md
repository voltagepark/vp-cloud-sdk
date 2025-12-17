# FleetNode

A node within a fleet (fleet_id not included as it's redundant in fleet context)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_name** | **str** | Unique identifier for the node | 
**state** | **str** | Current state of the node | 
**public_ip** | **str** | Public IP address of the node | 

## Example

```python
from vpcloud_client.models.fleet_node import FleetNode

# TODO update the JSON string below
json = "{}"
# create an instance of FleetNode from a JSON string
fleet_node_instance = FleetNode.from_json(json)
# print the JSON string representation of the object
print(FleetNode.to_json())

# convert the object into a dict
fleet_node_dict = fleet_node_instance.to_dict()
# create an instance of FleetNode from a dict
fleet_node_from_dict = FleetNode.from_dict(fleet_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


