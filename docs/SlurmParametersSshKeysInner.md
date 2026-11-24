# SlurmParametersSshKeysInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Username for SSH access | 
**keys** | **List[str]** | List of SSH public keys for this user | 

## Example

```python
from vpcloud_client.models.slurm_parameters_ssh_keys_inner import SlurmParametersSshKeysInner

# a SlurmParametersSshKeysInner as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of SlurmParametersSshKeysInner from a JSON string
slurm_parameters_ssh_keys_inner_instance = SlurmParametersSshKeysInner.from_json(json)
# print the JSON string representation of the object
print(slurm_parameters_ssh_keys_inner_instance.to_json())

# convert the object into a dict
slurm_parameters_ssh_keys_inner_dict = slurm_parameters_ssh_keys_inner_instance.to_dict()
# create an instance of SlurmParametersSshKeysInner from a dict
slurm_parameters_ssh_keys_inner_from_dict = SlurmParametersSshKeysInner.from_dict(slurm_parameters_ssh_keys_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


