# FleetNodeSpec


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instance_type** | **str** | Type of compute instance | 
**replicas** | **int** | Number of replicas (deprecated: use nodes array instead) | [optional] 
**reserved_nodes** | **List[str]** | List of reserved node identifiers (deprecated: use nodes array instead) | [optional] 
**nodes** | [**List[FleetNode]**](FleetNode.md) | List of actual node details with IPs | [optional] 

## Example

```python
from vpcloud_client.models.fleet_node_spec import FleetNodeSpec

# TODO update the JSON string below
json = "{}"
# create an instance of FleetNodeSpec from a JSON string
fleet_node_spec_instance = FleetNodeSpec.from_json(json)
# print the JSON string representation of the object
print(FleetNodeSpec.to_json())

# convert the object into a dict
fleet_node_spec_dict = fleet_node_spec_instance.to_dict()
# create an instance of FleetNodeSpec from a dict
fleet_node_spec_from_dict = FleetNodeSpec.from_dict(fleet_node_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


