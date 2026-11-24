# ExpandableCapacity


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**gpu_nodes** | [**ExpandableNodeSpec**](ExpandableNodeSpec.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.expandable_capacity import ExpandableCapacity

# a ExpandableCapacity as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of ExpandableCapacity from a JSON string
expandable_capacity_instance = ExpandableCapacity.from_json(json)
# print the JSON string representation of the object
print(expandable_capacity_instance.to_json())

# convert the object into a dict
expandable_capacity_dict = expandable_capacity_instance.to_dict()
# create an instance of ExpandableCapacity from a dict
expandable_capacity_from_dict = ExpandableCapacity.from_dict(expandable_capacity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


