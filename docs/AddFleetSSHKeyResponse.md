# AddFleetSSHKeyResponse

Acknowledgement that key propagation was accepted.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Human-readable outcome of the request. | 
**node_count** | **int** | Number of already-provisioned nodes the keys will be applied to. Zero means the fleet has no running nodes yet and the keys will arrive with cloud-init when its nodes deploy. | 

## Example

```python
from vpcloud_client.models.add_fleet_ssh_key_response import AddFleetSSHKeyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AddFleetSSHKeyResponse from a JSON string
add_fleet_ssh_key_response_instance = AddFleetSSHKeyResponse.from_json(json)
# print the JSON string representation of the object
print(AddFleetSSHKeyResponse.to_json())

# convert the object into a dict
add_fleet_ssh_key_response_dict = add_fleet_ssh_key_response_instance.to_dict()
# create an instance of AddFleetSSHKeyResponse from a dict
add_fleet_ssh_key_response_from_dict = AddFleetSSHKeyResponse.from_dict(add_fleet_ssh_key_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


