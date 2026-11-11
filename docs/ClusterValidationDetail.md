# ClusterValidationDetail

Typed view of a single cluster-validation run. The upstream validator's internal wire format is not exposed; callers code against the fields defined here.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**validation_id** | **int** | Cluster-validation run id. Use it to poll status, abort, or download logs. | 
**state** | **str** | Current run state. | 
**multi_host** | **bool** | Whether the run executes a single test across all selected nodes (multi-host) rather than one test per node. | [optional] 
**kubernetes** | **bool** | Whether the run uses Kubernetes-aware validation tests. Maps from the infrastructure service&#39;s k8s flag. | [optional] 
**node_names** | **List[str]** | Fleet node names included in this run. | [optional] 
**request_id** | **str** | Unique identifier for the underlying test request, when present. | [optional] 
**created_at** | **datetime** | When the run was created. | [optional] 
**start_time** | **datetime** | When the run became active. | [optional] 
**end_time** | **datetime** | When the run ended, when applicable. | [optional] 

## Example

```python
from vpcloud_client.models.cluster_validation_detail import ClusterValidationDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ClusterValidationDetail from a JSON string
cluster_validation_detail_instance = ClusterValidationDetail.from_json(json)
# print the JSON string representation of the object
print(ClusterValidationDetail.to_json())

# convert the object into a dict
cluster_validation_detail_dict = cluster_validation_detail_instance.to_dict()
# create an instance of ClusterValidationDetail from a dict
cluster_validation_detail_from_dict = ClusterValidationDetail.from_dict(cluster_validation_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


