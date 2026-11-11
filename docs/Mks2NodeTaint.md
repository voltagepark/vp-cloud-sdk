# Mks2NodeTaint

A taint on a live Kubernetes node (from the Kubernetes node spec). Identity is key+effect.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | Taint key. Maintenance uses voltagepark.io/maintenance. | 
**value** | **str** | Optional taint value. For &#x60;voltagepark.io/maintenance&#x60;, a value written through the managed Kubernetes node-taint API is the hold&#39;s end time in Unix seconds, and &#x60;true&#x60; means no end time. | [optional] 
**effect** | **str** | Taint effect. NoExecute is not exposed on the API write path. | 

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


