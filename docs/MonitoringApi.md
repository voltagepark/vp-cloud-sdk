# vpcloud_client.MonitoringApi

All URIs are relative to *https://api.sea1.voltagepark.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_fleet_grafana_dashboards**](MonitoringApi.md#get_fleet_grafana_dashboards) | **GET** /v1/fleets/{fleetId}/services/grafana | Get Grafana dashboards for a specific fleet
[**list_fleet_grafana_dashboards**](MonitoringApi.md#list_fleet_grafana_dashboards) | **GET** /v1/fleets/services/grafana | List Grafana dashboards for all fleets


# **get_fleet_grafana_dashboards**
> List[GrafanaDashboardResponse] get_fleet_grafana_dashboards(fleet_id)

Get Grafana dashboards for a specific fleet

Returns monitoring dashboards for a specific fleet. Each fleet can have multiple dashboards for different purposes (overview, detailed metrics, GPU performance, etc.).

**When to use:**
- Display available dashboards in your fleet detail view
- Show monitoring options to your users
- Embed dashboards in your application

**Important notes:**
- Empty array means no monitoring is configured for this fleet
- Users authenticate with Auth0 SSO when clicking dashboard links
- Dashboards automatically reflect current fleet state

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.grafana_dashboard_response import GrafanaDashboardResponse
from vpcloud_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.sea1.voltagepark.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vpcloud_client.Configuration(
    host = "https://api.sea1.voltagepark.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = vpcloud_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with vpcloud_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vpcloud_client.MonitoringApi(api_client)
    fleet_id = '900e8eac-2b1f-421f-a635-72556268b41f' # str | Fleet identifier

    try:
        # Get Grafana dashboards for a specific fleet
        api_response = api_instance.get_fleet_grafana_dashboards(fleet_id)
        print("The response of MonitoringApi->get_fleet_grafana_dashboards:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MonitoringApi->get_fleet_grafana_dashboards: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fleet_id** | **str**| Fleet identifier | 

### Return type

[**List[GrafanaDashboardResponse]**](GrafanaDashboardResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns array of available dashboards (empty if monitoring not configured) |  -  |
**404** | Fleet not found - check that the fleet ID is correct and belongs to your organization |  -  |
**401** | Unauthorized - invalid or missing authentication token |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_fleet_grafana_dashboards**
> List[GrafanaDashboardResponse] list_fleet_grafana_dashboards()

List Grafana dashboards for all fleets

Returns monitoring dashboards for all your active fleets. Use this endpoint to discover which fleets have Grafana monitoring configured.

**When to use:**
- Display monitoring availability in your fleet list view
- Discover which fleets have dashboards configured
- Check monitoring coverage across your organization

**Authentication:**
Dashboards use Auth0 SSO - users authenticate once with your credentials and gain automatic access to Grafana.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import vpcloud_client
from vpcloud_client.models.grafana_dashboard_response import GrafanaDashboardResponse
from vpcloud_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.sea1.voltagepark.com
# See configuration.py for a list of all supported configuration parameters.
configuration = vpcloud_client.Configuration(
    host = "https://api.sea1.voltagepark.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = vpcloud_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with vpcloud_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vpcloud_client.MonitoringApi(api_client)

    try:
        # List Grafana dashboards for all fleets
        api_response = api_instance.list_fleet_grafana_dashboards()
        print("The response of MonitoringApi->list_fleet_grafana_dashboards:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MonitoringApi->list_fleet_grafana_dashboards: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[GrafanaDashboardResponse]**](GrafanaDashboardResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success - returns array of dashboards (may be empty if no monitoring is configured) |  -  |
**401** | Unauthorized - invalid or missing authentication token |  -  |
**500** | Server error - please contact support if this persists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

