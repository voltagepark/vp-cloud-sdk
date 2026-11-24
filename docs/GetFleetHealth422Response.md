# GetFleetHealth422Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Error message describing why health cannot be retrieved | 
**fleet_id** | **str** | Unique identifier for the fleet | 
**status** | **str** | Current fleet status | 

## Example

```python
from vpcloud_client.models.get_fleet_health422_response import GetFleetHealth422Response

# a GetFleetHealth422Response as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of GetFleetHealth422Response from a JSON string
get_fleet_health422_response_instance = GetFleetHealth422Response.from_json(json)
# print the JSON string representation of the object
print(get_fleet_health422_response_instance.to_json())

# convert the object into a dict
get_fleet_health422_response_dict = get_fleet_health422_response_instance.to_dict()
# create an instance of GetFleetHealth422Response from a dict
get_fleet_health422_response_from_dict = GetFleetHealth422Response.from_dict(get_fleet_health422_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


