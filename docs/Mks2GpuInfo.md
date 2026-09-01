# Mks2GpuInfo

GPU information for an MKS-2 worker node.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of GPUs on the node. | [optional] 
**model** | **str** | GPU model name. | [optional] 
**driver_version** | **str** | NVIDIA driver version. | [optional] 
**cuda_runtime_version** | **str** | CUDA runtime version. | [optional] 
**memory** | **str** | Total GPU memory per device in MiB. | [optional] 
**validated** | **bool** | Whether GPU validation has passed for this node. | [optional] 

## Example

```python
from vpcloud_client.models.mks2_gpu_info import Mks2GpuInfo

# TODO update the JSON string below
json = "{}"
# create an instance of Mks2GpuInfo from a JSON string
mks2_gpu_info_instance = Mks2GpuInfo.from_json(json)
# print the JSON string representation of the object
print(Mks2GpuInfo.to_json())

# convert the object into a dict
mks2_gpu_info_dict = mks2_gpu_info_instance.to_dict()
# create an instance of Mks2GpuInfo from a dict
mks2_gpu_info_from_dict = Mks2GpuInfo.from_dict(mks2_gpu_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


