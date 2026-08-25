# Fleet

A fleet represents a cluster of GPU nodes provisioned for your workloads

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fleet_id** | **str** | Unique identifier for the fleet | 
**name** | **str** | Human-readable name for the fleet | 
**status** | [**FleetStatus**](FleetStatus.md) |  | 
**requested_at** | **int** | Timestamp when the fleet was requested (milliseconds since epoch UTC) | 
**provisioned_at** | **int** | Timestamp when the fleet was provisioned (milliseconds since epoch UTC) | [optional] 
**created_at** | **int** | Timestamp when the fleet was created in DDB (milliseconds since epoch UTC) | 
**updated_at** | **int** | Timestamp when the fleet was last updated in DDB (milliseconds since epoch UTC) | 
**compute_type** | **str** | Type of compute resources | 
**minimum_footprint** | [**FleetComputeFootprint**](FleetComputeFootprint.md) |  | 
**expandable_capacity** | [**ExpandableCapacity**](ExpandableCapacity.md) |  | [optional] 
**infrastructure** | [**Infrastructure**](Infrastructure.md) |  | 
**bootstrap** | [**Bootstrap**](Bootstrap.md) |  | 
**fleet_apps** | [**FleetApps**](FleetApps.md) |  | [optional] 
**os_config** | [**OsConfig**](OsConfig.md) |  | [optional] 
**order_id** | **str** | Linked order ID. Null if this fleet is not associated with an order. | [optional] 

## Example

```python
from vpcloud_client.models.fleet import Fleet

# TODO update the JSON string below
json = "{}"
# create an instance of Fleet from a JSON string
fleet_instance = Fleet.from_json(json)
# print the JSON string representation of the object
print(Fleet.to_json())

# convert the object into a dict
fleet_dict = fleet_instance.to_dict()
# create an instance of Fleet from a dict
fleet_from_dict = Fleet.from_dict(fleet_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


