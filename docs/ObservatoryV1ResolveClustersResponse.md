# ObservatoryV1ResolveClustersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**clusters** | [**List[ObservatoryV1ResolvedCluster]**](ObservatoryV1ResolvedCluster.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_resolve_clusters_response import ObservatoryV1ResolveClustersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1ResolveClustersResponse from a JSON string
observatory_v1_resolve_clusters_response_instance = ObservatoryV1ResolveClustersResponse.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1ResolveClustersResponse.to_json())

# convert the object into a dict
observatory_v1_resolve_clusters_response_dict = observatory_v1_resolve_clusters_response_instance.to_dict()
# create an instance of ObservatoryV1ResolveClustersResponse from a dict
observatory_v1_resolve_clusters_response_from_dict = ObservatoryV1ResolveClustersResponse.from_dict(observatory_v1_resolve_clusters_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


