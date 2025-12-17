# ExpandableNodeSpec


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instance_type** | **str** | Type of compute instance | 
**max_replicas** | **int** | Maximum number of replicas | 
**nodes** | [**List[FleetNode]**](FleetNode.md) | READ-ONLY: List of actual node details with IPs. This field is populated automatically during scaling operations and should not be provided in creation requests. | [optional] [readonly] 

## Example

```python
from vpcloud_client.models.expandable_node_spec import ExpandableNodeSpec

# TODO update the JSON string below
json = "{}"
# create an instance of ExpandableNodeSpec from a JSON string
expandable_node_spec_instance = ExpandableNodeSpec.from_json(json)
# print the JSON string representation of the object
print(ExpandableNodeSpec.to_json())

# convert the object into a dict
expandable_node_spec_dict = expandable_node_spec_instance.to_dict()
# create an instance of ExpandableNodeSpec from a dict
expandable_node_spec_from_dict = ExpandableNodeSpec.from_dict(expandable_node_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


