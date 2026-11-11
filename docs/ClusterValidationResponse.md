# ClusterValidationResponse

Status of a cluster-validation run. The API surfaces the documented fields; additional fields reported by the upstream validator may be included for forward compatibility and should not be relied on.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**validation_id** | **int** | Cluster-validation run id. Use it to poll status, abort, or download logs. | [optional] 
**status** | **str** | Current run status (e.g. RUNNING, COMPLETED, FAILED, ABORTED). | [optional] 

## Example

```python
from vpcloud_client.models.cluster_validation_response import ClusterValidationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ClusterValidationResponse from a JSON string
cluster_validation_response_instance = ClusterValidationResponse.from_json(json)
# print the JSON string representation of the object
print(ClusterValidationResponse.to_json())

# convert the object into a dict
cluster_validation_response_dict = cluster_validation_response_instance.to_dict()
# create an instance of ClusterValidationResponse from a dict
cluster_validation_response_from_dict = ClusterValidationResponse.from_dict(cluster_validation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


