# FleetHistoryEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_id** | **str** | Organization ID | 
**fleet_id** | **str** | Fleet ID | 
**source** | **str** | Source of the event, either &#x60;system&#x60; or &#x60;user&#x60;. | 
**current_state** | **str** | Current state after this event | 
**previous_state** | **str** | Previous state before this event | [optional] 
**event_timestamp** | **int** | Timestamp when the event occurred (milliseconds since epoch UTC) | 
**event_data** | **Dict[str, str]** | Additional event-specific data | [optional] 
**created_at** | **int** | Timestamp when the record was created | 
**schema_version** | **int** | Schema version | 

## Example

```python
from vpcloud_client.models.fleet_history_event import FleetHistoryEvent

# TODO update the JSON string below
json = "{}"
# create an instance of FleetHistoryEvent from a JSON string
fleet_history_event_instance = FleetHistoryEvent.from_json(json)
# print the JSON string representation of the object
print(FleetHistoryEvent.to_json())

# convert the object into a dict
fleet_history_event_dict = fleet_history_event_instance.to_dict()
# create an instance of FleetHistoryEvent from a dict
fleet_history_event_from_dict = FleetHistoryEvent.from_dict(fleet_history_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


