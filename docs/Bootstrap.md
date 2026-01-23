# Bootstrap

Bootstrap configuration for fleet nodes. Provide either sshUsers (recommended) or ssh-pub-keys for SSH access.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cloud_init** | **str** | Cloud-init script | [optional] 
**machine_image** | **str** | Machine image to use | 
**ssh_users** | **List[str]** | List of SSH usernames from your organization&#39;s SSH key management. Each user&#39;s public keys will be added and a corresponding Linux user will be created on each node. | [optional] 
**ssh_pub_keys** | **List[str]** | DEPRECATED: Use sshUsers instead. Raw keys for backward compatibility only. | [optional] 

## Example

```python
from vpcloud_client.models.bootstrap import Bootstrap

# TODO update the JSON string below
json = "{}"
# create an instance of Bootstrap from a JSON string
bootstrap_instance = Bootstrap.from_json(json)
# print the JSON string representation of the object
print(Bootstrap.to_json())

# convert the object into a dict
bootstrap_dict = bootstrap_instance.to_dict()
# create an instance of Bootstrap from a dict
bootstrap_from_dict = Bootstrap.from_dict(bootstrap_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


