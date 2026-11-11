# SSHKey

A user's SSH access record with multiple public keys

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ssh_key_id** | **str** | Unique identifier for this record | [optional] 
**username** | **str** | Linux username for SSH access and cloud-init | [optional] 
**public_keys** | [**List[PublicKeyEntry]**](PublicKeyEntry.md) | List of SSH public keys for this user | [optional] 
**created_at** | **int** | Creation timestamp (Unix milliseconds) | [optional] 

## Example

```python
from vpcloud_client.models.ssh_key import SSHKey

# TODO update the JSON string below
json = "{}"
# create an instance of SSHKey from a JSON string
ssh_key_instance = SSHKey.from_json(json)
# print the JSON string representation of the object
print(SSHKey.to_json())

# convert the object into a dict
ssh_key_dict = ssh_key_instance.to_dict()
# create an instance of SSHKey from a dict
ssh_key_from_dict = SSHKey.from_dict(ssh_key_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


