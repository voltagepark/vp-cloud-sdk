# GrafanaDashboardResponse

Monitoring dashboard information for a fleet. Each dashboard provides real-time metrics and visualizations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fleet_id** | **str** | Fleet identifier this dashboard monitors | 
**dashboard_id** | **str** | Dashboard type identifier - different dashboards show different levels of detail | 
**dashboard_url** | **str** | Direct link to view this dashboard in Grafana. Users authenticate via Auth0 SSO when opening the link. | 
**available** | **bool** | Indicates if the dashboard can be accessed. &#x60;false&#x60; means the fleet is not in ACTIVE state or monitoring is temporarily disabled. | 

## Example

```python
from vpcloud_client.models.grafana_dashboard_response import GrafanaDashboardResponse

# a GrafanaDashboardResponse as JSON, with the properties above, for example from an API response
json = "{}"
# create an instance of GrafanaDashboardResponse from a JSON string
grafana_dashboard_response_instance = GrafanaDashboardResponse.from_json(json)
# print the JSON string representation of the object
print(grafana_dashboard_response_instance.to_json())

# convert the object into a dict
grafana_dashboard_response_dict = grafana_dashboard_response_instance.to_dict()
# create an instance of GrafanaDashboardResponse from a dict
grafana_dashboard_response_from_dict = GrafanaDashboardResponse.from_dict(grafana_dashboard_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


