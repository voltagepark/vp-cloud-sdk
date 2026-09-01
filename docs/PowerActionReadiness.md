# PowerActionReadiness

Advisory readiness for disruptive power actions (ForceOff, GracefulShutdown, ForceRestart, GracefulRestart). Power On from Off is never gated by this object. `ready` means Harbor found no known blocker; warnings do not change readiness. The policy and user-facing copy are selected by API plane, while machine-readable blocker and warning codes remain internal for structured logging. Clients should not re-derive readiness from registrationStatus, schedulable, taints, or drained.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ready** | **bool** | True when Harbor found no known blocker. A non-empty warningMessage remains advisory and does not change this value. | 
**blocker_message** | **str** | Empty when ready. Otherwise contains the backend-owned, plane-appropriate explanation for the active blocker. Clients should display this complete sentence without parsing it. | 
**warning_message** | **str** | Empty when there are no warnings. Harbor composes active warning messages as complete sentences in deterministic order. Warnings are advisory and do not change ready. | 

## Example

```python
from vpcloud_client.models.power_action_readiness import PowerActionReadiness

# TODO update the JSON string below
json = "{}"
# create an instance of PowerActionReadiness from a JSON string
power_action_readiness_instance = PowerActionReadiness.from_json(json)
# print the JSON string representation of the object
print(PowerActionReadiness.to_json())

# convert the object into a dict
power_action_readiness_dict = power_action_readiness_instance.to_dict()
# create an instance of PowerActionReadiness from a dict
power_action_readiness_from_dict = PowerActionReadiness.from_dict(power_action_readiness_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


