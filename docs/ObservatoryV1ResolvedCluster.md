# ObservatoryV1ResolvedCluster


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cluster_id** | **str** |  | [optional] 
**endpoint** | **str** | Base URL of that region&#39;s endpoint. Send this cluster&#39;s queries there. | [optional] 
**logs_ready** | **bool** | Whether the cluster&#39;s logs can be queried yet. | [optional] [default to False]
**metrics_ready** | **bool** | Whether the cluster&#39;s metrics can be queried yet. | [optional] [default to False]
**site** | **str** | The region that serves the cluster&#39;s metrics and logs. | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_resolved_cluster import ObservatoryV1ResolvedCluster

# a ObservatoryV1ResolvedCluster as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of ObservatoryV1ResolvedCluster from a JSON string
observatory_v1_resolved_cluster_instance = ObservatoryV1ResolvedCluster.from_json(json)
# print the JSON string representation of the object
print(observatory_v1_resolved_cluster_instance.to_json())

# convert the object into a dict
observatory_v1_resolved_cluster_dict = observatory_v1_resolved_cluster_instance.to_dict()
# create an instance of ObservatoryV1ResolvedCluster from a dict
observatory_v1_resolved_cluster_from_dict = ObservatoryV1ResolvedCluster.from_dict(observatory_v1_resolved_cluster_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


