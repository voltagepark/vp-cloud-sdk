# CustomerTriggerClusterValidationRequest

Request to start a cluster-validation run against your fleet's nodes. Runs are always multi-host; that is not configurable.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_names** | **List[str]** | Optional subset of fleet node names to validate. Each name must belong to your fleet. Omit (or send an empty list) to validate all nodes in the fleet. | [optional] 
**kubernetes** | **bool** | When true, run Kubernetes-aware validation tests. Requires a Kubernetes-enabled fleet; the required cluster credential is obtained automatically and is never supplied by the caller. | [optional] [default to False]
**tests** | **List[str]** | Optional list of test names to run (from the cluster-validation test catalog). Omit to run the default set of tests. | [optional] 

## Example

```python
from vpcloud_client.models.customer_trigger_cluster_validation_request import CustomerTriggerClusterValidationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CustomerTriggerClusterValidationRequest from a JSON string
customer_trigger_cluster_validation_request_instance = CustomerTriggerClusterValidationRequest.from_json(json)
# print the JSON string representation of the object
print(CustomerTriggerClusterValidationRequest.to_json())

# convert the object into a dict
customer_trigger_cluster_validation_request_dict = customer_trigger_cluster_validation_request_instance.to_dict()
# create an instance of CustomerTriggerClusterValidationRequest from a dict
customer_trigger_cluster_validation_request_from_dict = CustomerTriggerClusterValidationRequest.from_dict(customer_trigger_cluster_validation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


