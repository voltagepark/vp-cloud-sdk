# SlurmParameters

Configuration parameters for SLURM addon

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ssh_keys** | [**List[SlurmParametersSshKeysInner]**](SlurmParametersSshKeysInner.md) | SSH user configurations with multiple keys per user | 
**external_storage** | [**ExternalStorageConfig**](ExternalStorageConfig.md) |  | 
**control_plane_nodes** | **List[str]** | Node IDs of the Slurm control-plane nodes. MKS labels these with slurm.voltagepark.io/node-role&#x3D;control-plane before activating the Helm chart. Install-only — optional at fleet creation; ignored if empty. | [optional] 
**login_nodes** | **List[str]** | Node IDs of the Slurm login nodes. MKS labels these with slurm.voltagepark.io/login-node&#x3D;true. Kept separate from controlPlaneNodes so a rogue login pod cannot disrupt slurmctld/slurmdbd. | [optional] 

## Example

```python
from vpcloud_client.models.slurm_parameters import SlurmParameters

# TODO update the JSON string below
json = "{}"
# create an instance of SlurmParameters from a JSON string
slurm_parameters_instance = SlurmParameters.from_json(json)
# print the JSON string representation of the object
print(SlurmParameters.to_json())

# convert the object into a dict
slurm_parameters_dict = slurm_parameters_instance.to_dict()
# create an instance of SlurmParameters from a dict
slurm_parameters_from_dict = SlurmParameters.from_dict(slurm_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


