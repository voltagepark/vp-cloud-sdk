# PublicKeyEntry

A single SSH public key with metadata

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fingerprint** | **str** | SHA256 fingerprint of the public key | [optional] 
**key** | **str** | SSH public key in OpenSSH format | [optional] 
**key_type** | **str** | SSH key algorithm type | [optional] 
**description** | **str** | Optional description for this key | [optional] 
**added_at** | **int** | When this key was added (Unix milliseconds) | [optional] 

## Example

```python
from vpcloud_client.models.public_key_entry import PublicKeyEntry

# TODO update the JSON string below
json = "{}"
# create an instance of PublicKeyEntry from a JSON string
public_key_entry_instance = PublicKeyEntry.from_json(json)
# print the JSON string representation of the object
print(PublicKeyEntry.to_json())

# convert the object into a dict
public_key_entry_dict = public_key_entry_instance.to_dict()
# create an instance of PublicKeyEntry from a dict
public_key_entry_from_dict = PublicKeyEntry.from_dict(public_key_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


