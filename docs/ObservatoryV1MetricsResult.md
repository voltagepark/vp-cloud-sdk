# ObservatoryV1MetricsResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result_json** | **bytearray** | Base64 of the Prometheus data.result JSON. | [optional] 
**result_type** | **str** | vector, matrix, scalar or string, as in Prometheus. | [optional] 

## Example

```python
from vpcloud_client.models.observatory_v1_metrics_result import ObservatoryV1MetricsResult

# TODO update the JSON string below
json = "{}"
# create an instance of ObservatoryV1MetricsResult from a JSON string
observatory_v1_metrics_result_instance = ObservatoryV1MetricsResult.from_json(json)
# print the JSON string representation of the object
print(ObservatoryV1MetricsResult.to_json())

# convert the object into a dict
observatory_v1_metrics_result_dict = observatory_v1_metrics_result_instance.to_dict()
# create an instance of ObservatoryV1MetricsResult from a dict
observatory_v1_metrics_result_from_dict = ObservatoryV1MetricsResult.from_dict(observatory_v1_metrics_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


