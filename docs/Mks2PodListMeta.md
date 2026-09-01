# Mks2PodListMeta

Pagination metadata for pod list responses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_cursor** | **str** | Opaque cursor for the next page (null when there are no more pages). | [optional] 

## Example

```python
from vpcloud_client.models.mks2_pod_list_meta import Mks2PodListMeta

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2PodListMeta from a JSON string
mks2_pod_list_meta_instance = Mks2PodListMeta.from_json(json)
# print the JSON string representation of the object
print(Mks2PodListMeta.to_json())

# convert the object into a dict
mks2_pod_list_meta_dict = mks2_pod_list_meta_instance.to_dict()
# create an instance of Mks2PodListMeta from a dict
mks2_pod_list_meta_from_dict = Mks2PodListMeta.from_dict(mks2_pod_list_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


