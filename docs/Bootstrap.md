# Bootstrap

Bootstrap configuration for fleet nodes. Provide either sshUsers (recommended) or ssh-pub-keys for SSH access.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cloud_init** | **str** | Node setup applied by cloud-init on every node, including nodes added by scaling. Accepts a script that starts with &#x60;#!&#x60;, a &#x60;#cloud-config&#x60; document, or plain shell commands, which run with bash. &#x60;#include&#x60;, &#x60;#cloud-boothook&#x60;, Jinja templates, &#x60;#part-handler&#x60;, MIME multi-part, and compressed content are rejected. A &#x60;#cloud-config&#x60; document must be a single YAML mapping that cloud-init can load; if it sets &#x60;users&#x60;, that must be a list of names or user mappings. It must not configure disks or filesystems, change cloud-init&#39;s module lists, or mount over or inside system directories or the fleet&#39;s storage mount points; mount paths must not contain &#x60;..&#x60;. | [optional] 
**machine_image** | **str** | Machine image to use. On a Managed Kubernetes v2 fleet, an image whose name marks it as built for a different CPU architecture (amd64 or arm64) than the selected nodes is rejected. | 
**ssh_users** | **List[str]** | List of SSH usernames from your organization&#39;s SSH key management. Each user&#39;s public keys will be added and a corresponding Linux user will be created on each node. | [optional] 
**ssh_pub_keys** | **List[str]** | DEPRECATED: Use sshUsers instead. Raw keys for backward compatibility only. | [optional] 
**sudo_access** | **str** | Controls sudo access for the SSH users the API creates on every node in the fleet (both sshUsers and the deprecated ssh-pub-keys path). When enabled, each API-managed user is granted passwordless sudo; when disabled, users are created without any API-managed sudo rule. Applies to standalone bare-metal fleets and is fixed at creation time. Defaults to enabled. | [optional] 

## Example

```python
from vpcloud_client.models.bootstrap import Bootstrap

# TODO update the JSON string below
json = "{}"
# create an instance of Bootstrap from a JSON string
bootstrap_instance = Bootstrap.from_json(json)
# print the JSON string representation of the object
print(Bootstrap.to_json())

# convert the object into a dict
bootstrap_dict = bootstrap_instance.to_dict()
# create an instance of Bootstrap from a dict
bootstrap_from_dict = Bootstrap.from_dict(bootstrap_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


