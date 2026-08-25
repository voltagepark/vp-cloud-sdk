# StorageProtectionPolicy

Optional snapshot protection policy applied when first provisioning a storage view.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_at** | **datetime** | ISO 8601 datetime to start the protection policy. | [optional] 
**every** | **str** | Snapshot frequency (e.g., &#39;15m&#39; for every 15 minutes). | [optional] 
**keep_local** | **str** | Duration to keep local snapshots (e.g., &#39;10h&#39;). | [optional] 
**keep_remote** | **str** | Duration to keep remote snapshots (e.g., &#39;0s&#39; for none). | [optional] 

## Example

```python
from vpcloud_client.models.storage_protection_policy import StorageProtectionPolicy

# TODO update the JSON string below
json = "{}"
# create an instance of StorageProtectionPolicy from a JSON string
storage_protection_policy_instance = StorageProtectionPolicy.from_json(json)
# print the JSON string representation of the object
print(StorageProtectionPolicy.to_json())

# convert the object into a dict
storage_protection_policy_dict = storage_protection_policy_instance.to_dict()
# create an instance of StorageProtectionPolicy from a dict
storage_protection_policy_from_dict = StorageProtectionPolicy.from_dict(storage_protection_policy_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


