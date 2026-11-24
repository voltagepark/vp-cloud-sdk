# FleetComputeFootprint


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**gpu_nodes** | [**FleetNodeSpec**](FleetNodeSpec.md) |  | 

## Example

```python
from vpcloud_client.models.fleet_compute_footprint import FleetComputeFootprint

# a FleetComputeFootprint as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of FleetComputeFootprint from a JSON string
fleet_compute_footprint_instance = FleetComputeFootprint.from_json(json)
# print the JSON string representation of the object
print(fleet_compute_footprint_instance.to_json())

# convert the object into a dict
fleet_compute_footprint_dict = fleet_compute_footprint_instance.to_dict()
# create an instance of FleetComputeFootprint from a dict
fleet_compute_footprint_from_dict = FleetComputeFootprint.from_dict(fleet_compute_footprint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


