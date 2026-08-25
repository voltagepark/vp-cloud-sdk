# GrafanaLogsResponse

Dashboard and Explore deep-links for a fleet's VictoriaLogs datasource in Harbor Grafana.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fleet_id** | **str** | Fleet identifier these logs belong to | 
**available** | **bool** | Indicates if logs links can be used. &#x60;false&#x60; means the fleet is not ACTIVE (links may still be returned for transitional states). | 
**datasource_name** | **str** | Grafana datasource display name for this fleet&#39;s VictoriaLogs datasource (&#x60;{fleetName}-logs&#x60;). UID remains the fleet id. | 
**dashboard_url** | **str** | Direct link to the Harbor K8s system-logs Dashboard with this fleet&#39;s Logs datasource pre-selected. Prefer this over Explore for the default UX. | 
**explore_url** | **str** | Direct link to Grafana Explore pre-selecting this fleet&#39;s Logs datasource. Users authenticate via Auth0 SSO when opening the link. | 

## Example

```python
from vpcloud_client.models.grafana_logs_response import GrafanaLogsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GrafanaLogsResponse from a JSON string
grafana_logs_response_instance = GrafanaLogsResponse.from_json(json)
# print the JSON string representation of the object
print(GrafanaLogsResponse.to_json())

# convert the object into a dict
grafana_logs_response_dict = grafana_logs_response_instance.to_dict()
# create an instance of GrafanaLogsResponse from a dict
grafana_logs_response_from_dict = GrafanaLogsResponse.from_dict(grafana_logs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


