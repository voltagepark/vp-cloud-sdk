# AddFleetSSHKeyRequest

Identifies the already-registered SSH key to apply to the fleet.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ssh_key_id** | **str** | Identifier of an SSH key record in the caller&#39;s organization. Every public key held by that record is applied. | 

## Example

```python
from vpcloud_client.models.add_fleet_ssh_key_request import AddFleetSSHKeyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddFleetSSHKeyRequest from a JSON string
add_fleet_ssh_key_request_instance = AddFleetSSHKeyRequest.from_json(json)
# print the JSON string representation of the object
print(AddFleetSSHKeyRequest.to_json())

# convert the object into a dict
add_fleet_ssh_key_request_dict = add_fleet_ssh_key_request_instance.to_dict()
# create an instance of AddFleetSSHKeyRequest from a dict
add_fleet_ssh_key_request_from_dict = AddFleetSSHKeyRequest.from_dict(add_fleet_ssh_key_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


