# NodePowerState

Eventually consistent power state for a node. powerState is the last confirmed value and can lag the hardware while a power operation is in progress, or until the confirmation is older than 5 minutes. lastOperation shows the status of the most recent power operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** | Node identifier. | 
**power_state** | **str** | Last confirmed power state. Eventually consistent: it can lag the hardware while a power operation is in progress, and it is refreshed from the hardware when the confirmation is older than 5 minutes. | 
**last_operation** | [**NodePowerLastOperation**](NodePowerLastOperation.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.node_power_state import NodePowerState

# TODO update the JSON string below
json = "{}"
# create an instance of NodePowerState from a JSON string
node_power_state_instance = NodePowerState.from_json(json)
# print the JSON string representation of the object
print(NodePowerState.to_json())

# convert the object into a dict
node_power_state_dict = node_power_state_instance.to_dict()
# create an instance of NodePowerState from a dict
node_power_state_from_dict = NodePowerState.from_dict(node_power_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


