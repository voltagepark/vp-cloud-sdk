# Mks2NodeMaintenance

Maintenance state of the node, read from the live Kubernetes node on every request. The `voltagepark.io/maintenance` taint keeps new pods off the node, and the `MaintenanceWindow` node condition pauses Voltage Park's per-node health alerts. Changes made outside this API (kubectl, automation, a hold expiring) show up on the next read.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active** | **bool** | Whether a maintenance taint holds the node now: one is present and either has no end time or ends in the future. An expired taint is reported as inactive even while it waits to be removed. | 
**kind** | **str** | What holds the node. &#x60;timed&#x60; ends at &#x60;until&#x60; and is removed automatically after it expires. &#x60;indefinite&#x60; has no end time and stays until someone removes it, for example a taint applied with &#x60;kubectl taint node &lt;node&gt; voltagepark.io/maintenance&#x3D;true:NoSchedule&#x60;. &#x60;validationHold&#x60; keeps a newly joined node out of service until it passes GPU validation. When the node carries more than one maintenance taint, the one in force is reported, preferring &#x60;validationHold&#x60;, then &#x60;indefinite&#x60;, then the &#x60;timed&#x60; one that ends last. Absent when the node carries no maintenance taint. | [optional] 
**effect** | **str** | Effect of the reported maintenance taint. Absent when the node carries no maintenance taint. | [optional] 
**until** | **datetime** | When a &#x60;timed&#x60; hold ends. A time in the past means the hold has expired and is waiting to be removed. | [optional] 
**alert_suppression** | [**Mks2NodeAlertSuppression**](Mks2NodeAlertSuppression.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.mks2_node_maintenance import Mks2NodeMaintenance

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2NodeMaintenance from a JSON string
mks2_node_maintenance_instance = Mks2NodeMaintenance.from_json(json)
# print the JSON string representation of the object
print(Mks2NodeMaintenance.to_json())

# convert the object into a dict
mks2_node_maintenance_dict = mks2_node_maintenance_instance.to_dict()
# create an instance of Mks2NodeMaintenance from a dict
mks2_node_maintenance_from_dict = Mks2NodeMaintenance.from_dict(mks2_node_maintenance_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


