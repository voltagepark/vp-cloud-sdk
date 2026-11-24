# NodeHealth


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** | Unique identifier for the node | 
**status** | **str** | Health status of the node | 
**last_updated_at** | **int** | Timestamp when the node health was last updated (milliseconds since epoch UTC) | 

## Example

```python
from vpcloud_client.models.node_health import NodeHealth

# a NodeHealth as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of NodeHealth from a JSON string
node_health_instance = NodeHealth.from_json(json)
# print the JSON string representation of the object
print(node_health_instance.to_json())

# convert the object into a dict
node_health_dict = node_health_instance.to_dict()
# create an instance of NodeHealth from a dict
node_health_from_dict = NodeHealth.from_dict(node_health_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


