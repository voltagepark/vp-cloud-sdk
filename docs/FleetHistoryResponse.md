# FleetHistoryResponse

Response containing fleet history events with optional pagination metadata

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fleet_id** | **str** | Unique identifier for the fleet | 
**events** | [**List[FleetHistoryEvent]**](FleetHistoryEvent.md) | List of fleet history events, newest first | 
**next_token** | **str** | Pagination token to retrieve the next page of results. Null when no more pages available. | [optional] 

## Example

```python
from vpcloud_client.models.fleet_history_response import FleetHistoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FleetHistoryResponse from a JSON string
fleet_history_response_instance = FleetHistoryResponse.from_json(json)
# print the JSON string representation of the object
print(FleetHistoryResponse.to_json())

# convert the object into a dict
fleet_history_response_dict = fleet_history_response_instance.to_dict()
# create an instance of FleetHistoryResponse from a dict
fleet_history_response_from_dict = FleetHistoryResponse.from_dict(fleet_history_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


