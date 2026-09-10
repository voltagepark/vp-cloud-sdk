# FleetHealthResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fleet_id** | **str** | Unique identifier for the fleet | 
**status** | **str** | Overall health status of the fleet | [optional] 
**kubernetes_health** | **Dict[str, object]** | Legacy managed Kubernetes cluster health information | [optional] 
**node_health** | [**List[NodeHealth]**](NodeHealth.md) | Health information for each node in the fleet | [optional] 

## Example

```python
from vpcloud_client.models.fleet_health_response import FleetHealthResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FleetHealthResponse from a JSON string
fleet_health_response_instance = FleetHealthResponse.from_json(json)
# print the JSON string representation of the object
print(FleetHealthResponse.to_json())

# convert the object into a dict
fleet_health_response_dict = fleet_health_response_instance.to_dict()
# create an instance of FleetHealthResponse from a dict
fleet_health_response_from_dict = FleetHealthResponse.from_dict(fleet_health_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


