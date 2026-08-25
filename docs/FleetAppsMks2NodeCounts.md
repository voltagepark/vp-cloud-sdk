# FleetAppsMks2NodeCounts

Aggregate count summary of worker node status in the MKS-2 cluster. Mirrors mks2sdk.NodeCounts. All counters are required to keep the parent FleetAppsMks2Cluster atomic-or-absent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** | Total number of registered nodes | 
**ready** | **int** | Nodes that are Ready in the Kubernetes sense | 
**not_ready** | **int** | Nodes that are registered but not Ready | 
**pending** | **int** | Nodes registered in MKS but not yet joined to Kubernetes | 

## Example

```python
from vpcloud_client.models.fleet_apps_mks2_node_counts import FleetAppsMks2NodeCounts

# TODO update the JSON string below
json = "{}"
# create an instance of FleetAppsMks2NodeCounts from a JSON string
fleet_apps_mks2_node_counts_instance = FleetAppsMks2NodeCounts.from_json(json)
# print the JSON string representation of the object
print(FleetAppsMks2NodeCounts.to_json())

# convert the object into a dict
fleet_apps_mks2_node_counts_dict = fleet_apps_mks2_node_counts_instance.to_dict()
# create an instance of FleetAppsMks2NodeCounts from a dict
fleet_apps_mks2_node_counts_from_dict = FleetAppsMks2NodeCounts.from_dict(fleet_apps_mks2_node_counts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


