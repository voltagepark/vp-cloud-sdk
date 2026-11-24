# KubernetesServiceLinks

Links to Kubernetes cluster services

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**grafana** | **str** | URL to the Grafana dashboard for cluster monitoring | [optional] 

## Example

```python
from vpcloud_client.models.kubernetes_service_links import KubernetesServiceLinks

# a KubernetesServiceLinks as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of KubernetesServiceLinks from a JSON string
kubernetes_service_links_instance = KubernetesServiceLinks.from_json(json)
# print the JSON string representation of the object
print(kubernetes_service_links_instance.to_json())

# convert the object into a dict
kubernetes_service_links_dict = kubernetes_service_links_instance.to_dict()
# create an instance of KubernetesServiceLinks from a dict
kubernetes_service_links_from_dict = KubernetesServiceLinks.from_dict(kubernetes_service_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


