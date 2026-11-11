# Mks2HealthStatus

Health state for any managed Kubernetes component, node, or the cluster overall. `healthy` = all observed signals are nominal; `degraded` = partial functionality, some signals failing; `unhealthy` = no usable functionality from this component; `stopped` = intentionally scaled to zero (e.g. control plane replicas == 0); `unknown` = no signal available yet (probe pending, monitor not wired, etc.).

## Enum

* `HEALTHY` (value: `'healthy'`)

* `DEGRADED` (value: `'degraded'`)

* `UNHEALTHY` (value: `'unhealthy'`)

* `STOPPED` (value: `'stopped'`)

* `UNKNOWN` (value: `'unknown'`)

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


