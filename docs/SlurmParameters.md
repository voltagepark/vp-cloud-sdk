# SlurmParameters

Configuration parameters for SLURM addon

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ssh_keys** | [**List[SlurmParametersSshKeysInner]**](SlurmParametersSshKeysInner.md) | SSH user configurations with multiple keys per user | 
**external_storage** | [**ExternalStorageConfig**](ExternalStorageConfig.md) |  | 
**control_plane_nodes** | **List[str]** | Node IDs of the Slurm control-plane nodes. These nodes are labeled with slurm.voltagepark.io/node-role&#x3D;control-plane before activating the Helm chart. Install-only — optional at fleet creation; ignored if empty. | [optional] 
**control_plane_placement** | **str** | Whether the control-plane nodes also run Slurm jobs. shared: they run a worker too, so one GPU node is a complete Slurm cluster; give 1 or 2 controlPlaneNodes (when omitted, the first GPU node not listed in loginNodes, or the first GPU node if all are). dedicated: they run only Slurm&#39;s controllers, and at least one GPU node must remain a worker. When omitted: dedicated if controlPlaneNodes is set, otherwise shared. | [optional] 
**slurm_version** | **str** | Slurm major version to install: 24 or 26. When omitted, the default applies: Slurm 26 wherever it is available, otherwise Slurm 24. Slurm 24 is not available on arm64 (GB300) nodes, so asking for it there is rejected. It applies at install: a fleet on Slurm 24 can later be upgraded in place to Slurm 26 from its Slurm tab, which updates this value. | [optional] 
**login_nodes** | **List[str]** | Node IDs of the Slurm login nodes. These nodes are labeled with slurm.voltagepark.io/login-node&#x3D;true. Kept separate from controlPlaneNodes so a rogue login pod cannot disrupt slurmctld/slurmdbd. | [optional] 

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


