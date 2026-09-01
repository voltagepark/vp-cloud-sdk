# NodeManagedServices

Managed-service overlays for this physical node. Omit the entire object when no managed service resolves (e.g. non-MKS fleet or name-lookup miss).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kubernetes** | [**Mks2WorkerNodeDetail**](Mks2WorkerNodeDetail.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.node_managed_services import NodeManagedServices

# TODO update the JSON string below
json = "{}"
# create an instance of NodeManagedServices from a JSON string
node_managed_services_instance = NodeManagedServices.from_json(json)
# print the JSON string representation of the object
print(NodeManagedServices.to_json())

# convert the object into a dict
node_managed_services_dict = node_managed_services_instance.to_dict()
# create an instance of NodeManagedServices from a dict
node_managed_services_from_dict = NodeManagedServices.from_dict(node_managed_services_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


