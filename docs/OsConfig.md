# OsConfig

Declarative, intent-based OS tuning applied to the operating system of every node in the fleet. Each capability is requested by name; Harbor owns the known-good translation to node-level configuration and re-applies it on scale-up so new nodes inherit the same tuning. All capabilities are optional; omit the whole object to keep node OS defaults.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cpu_profiling** | **str** | Enable non-root, system-wide CPU profiling on every node (e.g. &#x60;perf top&#x60;, &#x60;perf stat -a&#x60;). When enabled, Harbor applies the required node kernel settings automatically. Defaults to disabled. | [optional] 

## Example

```python
from vpcloud_client.models.os_config import OsConfig

# TODO update the JSON string below
json = "{}"
# create an instance of OsConfig from a JSON string
os_config_instance = OsConfig.from_json(json)
# print the JSON string representation of the object
print(OsConfig.to_json())

# convert the object into a dict
os_config_dict = os_config_instance.to_dict()
# create an instance of OsConfig from a dict
os_config_from_dict = OsConfig.from_dict(os_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


