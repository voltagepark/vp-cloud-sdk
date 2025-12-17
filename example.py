import os
import json
import {vpcloud_client}
from {vpcloud_client}.rest import ApiException

# Configure Auth0 M2M authentication using client credentials
# The SDK will automatically exchange these for an access token
# Defining the host is optional and defaults to https://api.sea1.voltagepark.com
# See configuration.py for a list of all supported configuration parameters.
configuration = {vpcloud_client}.Configuration(
    host = "https://api.sea1.voltagepark.com",
    client_id = os.environ["VPCLOUD_CLIENT_ID"],
    client_secret = os.environ["VPCLOUD_CLIENT_SECRET"]
)

# Enter a context with an instance of the API client
with {vpcloud_client}.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = {vpcloud_client}.FleetsApi(api_client)

    try:
        # List your fleets
        api_response = api_instance.list_fleets()
        print("The response of FleetsApi->list_fleets:\n")
        # Convert response to dict for cleaner output
        print(json.dumps(api_response.model_dump(), indent=2))
    except ApiException as e:
        print("Exception when calling FleetsApi->list_fleets: %s\n" % e)

