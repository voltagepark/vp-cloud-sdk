# KubeconfigV2Response

Time-limited kubeconfig credential for a managed Kubernetes cluster. Returned by the customer kubeconfig endpoint as a short-lived, customer-scoped credential; refetch before `expiresAt`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kubeconfig** | **str** | Complete kubeconfig YAML, ready to be written to disk and consumed by kubectl. Server URL points at the external cluster API endpoint. | 
**role** | **str** | Role this kubeconfig was generated for. Customer-scoped kubeconfigs return &#x60;customer&#x60;. | 
**expires_at** | **datetime** | Absolute time at which the kubeconfig stops working. Clients should refetch before this expires. | 
**ttl_seconds** | **int** | Time-to-live in seconds from the moment the kubeconfig was generated. Convenience hint - prefer expiresAt for absolute scheduling. | 

## Example

```python
from vpcloud_client.models.kubeconfig_v2_response import KubeconfigV2Response

# TODO update the JSON string below
json = "{}"
# create an instance of KubeconfigV2Response from a JSON string
kubeconfig_v2_response_instance = KubeconfigV2Response.from_json(json)
# print the JSON string representation of the object
print(KubeconfigV2Response.to_json())

# convert the object into a dict
kubeconfig_v2_response_dict = kubeconfig_v2_response_instance.to_dict()
# create an instance of KubeconfigV2Response from a dict
kubeconfig_v2_response_from_dict = KubeconfigV2Response.from_dict(kubeconfig_v2_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


