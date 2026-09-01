# Mks2PodList

Pod list response. `items` carries the page contents and `meta.nextCursor` carries the opaque continuation token for the next page (null when there are no more pages).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[Mks2Pod]**](Mks2Pod.md) | Pods in the current page. Empty array (not null) when the cluster has no matching pods. | 
**meta** | [**Mks2PodListMeta**](Mks2PodListMeta.md) |  | [optional] 

## Example

```python
from vpcloud_client.models.mks2_pod_list import Mks2PodList

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2PodList from a JSON string
mks2_pod_list_instance = Mks2PodList.from_json(json)
# print the JSON string representation of the object
print(Mks2PodList.to_json())

# convert the object into a dict
mks2_pod_list_dict = mks2_pod_list_instance.to_dict()
# create an instance of Mks2PodList from a dict
mks2_pod_list_from_dict = Mks2PodList.from_dict(mks2_pod_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


