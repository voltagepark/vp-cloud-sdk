# RemoveFleetSSHKeyResponse

Acknowledgement that key revocation was accepted.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Human-readable outcome of the request. | 
**node_count** | **int** | Number of already-provisioned nodes the keys will be removed from. Zero means the fleet has no running nodes yet. | 

## Example

```python
from vpcloud_client.models.remove_fleet_ssh_key_response import RemoveFleetSSHKeyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RemoveFleetSSHKeyResponse from a JSON string
remove_fleet_ssh_key_response_instance = RemoveFleetSSHKeyResponse.from_json(json)
# print the JSON string representation of the object
print(RemoveFleetSSHKeyResponse.to_json())

# convert the object into a dict
remove_fleet_ssh_key_response_dict = remove_fleet_ssh_key_response_instance.to_dict()
# create an instance of RemoveFleetSSHKeyResponse from a dict
remove_fleet_ssh_key_response_from_dict = RemoveFleetSSHKeyResponse.from_dict(remove_fleet_ssh_key_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


