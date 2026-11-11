# ClusterValidationListResponse

A bounded, newest-first list of recent cluster-validation runs for a fleet (capped at 10).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[ClusterValidationDetail]**](ClusterValidationDetail.md) | Recent runs, newest first. Empty array (not null) when the fleet has no runs. | 

## Example

```python
from vpcloud_client.models.cluster_validation_list_response import ClusterValidationListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ClusterValidationListResponse from a JSON string
cluster_validation_list_response_instance = ClusterValidationListResponse.from_json(json)
# print the JSON string representation of the object
print(ClusterValidationListResponse.to_json())

# convert the object into a dict
cluster_validation_list_response_dict = cluster_validation_list_response_instance.to_dict()
# create an instance of ClusterValidationListResponse from a dict
cluster_validation_list_response_from_dict = ClusterValidationListResponse.from_dict(cluster_validation_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


