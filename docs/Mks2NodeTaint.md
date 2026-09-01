# Mks2NodeTaint

A taint on a live Kubernetes node (from MKS Spec.Taints). Identity is key+effect.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | Taint key. Maintenance uses voltagepark.io/maintenance. | 
**value** | **str** | Optional taint value. Maintenance convention is \&quot;true\&quot;. | [optional] 
**effect** | **str** | Taint effect. NoExecute is not exposed on the Harbor write path. | 

## Example

```python
from vpcloud_client.models.mks2_node_taint import Mks2NodeTaint

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2NodeTaint from a JSON string
mks2_node_taint_instance = Mks2NodeTaint.from_json(json)
# print the JSON string representation of the object
print(Mks2NodeTaint.to_json())

# convert the object into a dict
mks2_node_taint_dict = mks2_node_taint_instance.to_dict()
# create an instance of Mks2NodeTaint from a dict
mks2_node_taint_from_dict = Mks2NodeTaint.from_dict(mks2_node_taint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


