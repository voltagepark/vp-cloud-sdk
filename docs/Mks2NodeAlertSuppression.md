# Mks2NodeAlertSuppression

The node's `MaintenanceWindow` condition, which pauses Voltage Park's per-node health alerts for the node until `until`. It opens when maintenance is declared through the platform API, closes when that maintenance is ended, and otherwise expires on its own. Absent when the node has no such condition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active** | **bool** | Whether alerts are paused now: the condition is True and &#x60;until&#x60; is in the future. | 
**reason** | **str** | Category of the caller that opened the window, as recorded on the node, for example &#x60;OnCall&#x60; for an on-call engineer. | [optional] 
**opened_by** | **str** | Audit identity recorded for the window, as &#x60;&lt;service&gt;/&lt;user&gt;&#x60; where the user is known. | [optional] 
**since** | **datetime** | When the window started. | [optional] 
**until** | **datetime** | When the window ends, or ended. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_node_alert_suppression import Mks2NodeAlertSuppression

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2NodeAlertSuppression from a JSON string
mks2_node_alert_suppression_instance = Mks2NodeAlertSuppression.from_json(json)
# print the JSON string representation of the object
print(Mks2NodeAlertSuppression.to_json())

# convert the object into a dict
mks2_node_alert_suppression_dict = mks2_node_alert_suppression_instance.to_dict()
# create an instance of Mks2NodeAlertSuppression from a dict
mks2_node_alert_suppression_from_dict = Mks2NodeAlertSuppression.from_dict(mks2_node_alert_suppression_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


