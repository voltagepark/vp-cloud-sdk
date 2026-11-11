# CreateSSHKeyRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** | Linux username (POSIX-compliant). 1-32 chars, starts with letter/underscore. | 
**public_key** | **str** | SSH public key in any standard format. Will be normalized to OpenSSH format. | 
**description** | **str** | Optional description for this key (e.g., &#39;MacBook Pro&#39;) | [optional] 

## Example

```python
from vpcloud_client.models.create_ssh_key_request import CreateSSHKeyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSSHKeyRequest from a JSON string
create_ssh_key_request_instance = CreateSSHKeyRequest.from_json(json)
# print the JSON string representation of the object
print(CreateSSHKeyRequest.to_json())

# convert the object into a dict
create_ssh_key_request_dict = create_ssh_key_request_instance.to_dict()
# create an instance of CreateSSHKeyRequest from a dict
create_ssh_key_request_from_dict = CreateSSHKeyRequest.from_dict(create_ssh_key_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


