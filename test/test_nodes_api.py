# coding: utf-8

"""
    Voltage Park Cloud API — NodesApi unit tests.

    Tests the SDK client layer for node details, power state, and listing.
    All HTTP calls are mocked so no real API traffic is generated.
"""

import json

import pytest
from unittest.mock import patch

from vpcloud_client.api.nodes_api import NodesApi
from vpcloud_client.models.node_details import NodeDetails
from vpcloud_client.models.node_power_state import NodePowerState
from vpcloud_client.models.list_nodes_response import ListNodesResponse
from vpcloud_client.rest import ApiException
from vpcloud_client import ApiClient
from test.utils import create_test_config, MockResponse

FLEET_ID = "00000000-0000-0000-0000-000000000001"
NODE_ID = "node-abc-123"


class TestNodesApi:
    """NodesApi unit tests"""

    @pytest.fixture
    def api_instance(self):
        """Create API instance for testing."""
        config = create_test_config()
        return NodesApi(api_client=ApiClient(config))

    # ------------------------------------------------------------------
    # get_fleet_node_details
    # ------------------------------------------------------------------

    def test_get_fleet_node_details_success(self, api_instance):
        """Retrieve consolidated node details with power readiness."""
        body = {
            "nodeName": NODE_ID,
            "state": "ACTIVE",
            "publicIp": "1.2.3.4",
            "fleetId": FLEET_ID,
            "powerActionReadiness": {
                "ready": True,
                "blockerMessage": "",
                "warningMessage": "",
            },
        }
        mock_response = MockResponse(
            200,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            result = api_instance.get_fleet_node_details(FLEET_ID, NODE_ID)
            assert isinstance(result, NodeDetails)
            assert result.node_name == NODE_ID
            assert result.power_action_readiness.ready is True
            assert result.power_action_readiness.blocker_message == ""

    def test_get_fleet_node_details_not_ready(self, api_instance):
        """Node details when power readiness has a blocker."""
        body = {
            "nodeName": NODE_ID,
            "state": "ACTIVE",
            "publicIp": "1.2.3.4",
            "fleetId": FLEET_ID,
            "powerActionReadiness": {
                "ready": False,
                "blockerMessage": "Node is not drained.",
                "warningMessage": "",
            },
        }
        mock_response = MockResponse(
            200,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            result = api_instance.get_fleet_node_details(FLEET_ID, NODE_ID)
            assert result.power_action_readiness.ready is False
            assert "not drained" in result.power_action_readiness.blocker_message

    def test_get_fleet_node_details_error(self, api_instance):
        """404 when node does not exist."""
        mock_response = MockResponse(
            404,
            data=b'{"error": "not found"}',
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            with pytest.raises(ApiException) as exc_info:
                api_instance.get_fleet_node_details(FLEET_ID, NODE_ID)
            assert exc_info.value.status == 404

    # ------------------------------------------------------------------
    # get_node_power_state
    # ------------------------------------------------------------------

    def test_get_node_power_state_success(self, api_instance):
        """Retrieve live power state with last operation."""
        body = {
            "nodeId": NODE_ID,
            "powerState": "On",
            "lastOperation": {
                "operationId": "op-123",
                "resetType": "ForceRestart",
                "status": "SUCCESS",
                "queuedAt": 1700000000000,
                "completedAt": 1700000060000,
                "verifiedPowerState": "On",
            },
        }
        mock_response = MockResponse(
            200,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            result = api_instance.get_node_power_state(FLEET_ID, NODE_ID)
            assert isinstance(result, NodePowerState)
            assert result.power_state == "On"
            assert result.last_operation is not None
            assert result.last_operation.status == "SUCCESS"
            assert result.last_operation.operation_id == "op-123"

    def test_get_node_power_state_no_operation(self, api_instance):
        """Power state without any previous operation."""
        body = {
            "nodeId": NODE_ID,
            "powerState": "On",
        }
        mock_response = MockResponse(
            200,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            result = api_instance.get_node_power_state(FLEET_ID, NODE_ID)
            assert result.power_state == "On"
            assert result.last_operation is None

    def test_get_node_power_state_in_progress(self, api_instance):
        """Power state while an operation is in progress."""
        body = {
            "nodeId": NODE_ID,
            "powerState": "On",
            "lastOperation": {
                "operationId": "op-456",
                "resetType": "ForceRestart",
                "status": "IN_PROGRESS",
                "queuedAt": 1700000000000,
            },
        }
        mock_response = MockResponse(
            200,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            result = api_instance.get_node_power_state(FLEET_ID, NODE_ID)
            assert result.last_operation.status == "IN_PROGRESS"
            assert result.last_operation.completed_at is None

    def test_get_node_power_state_error(self, api_instance):
        """Error fetching power state."""
        mock_response = MockResponse(
            500,
            data=b'{"error": "internal server error"}',
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            with pytest.raises(ApiException) as exc_info:
                api_instance.get_node_power_state(FLEET_ID, NODE_ID)
            assert exc_info.value.status == 500

    # ------------------------------------------------------------------
    # get_node_by_fleet_id
    # ------------------------------------------------------------------

    def test_get_node_by_fleet_id_success(self, api_instance):
        """Retrieve a single node by fleet and node ID."""
        body = {
            "nodeName": NODE_ID,
            "state": "ACTIVE",
            "publicIp": "1.2.3.4",
            "fleetId": FLEET_ID,
        }
        mock_response = MockResponse(
            200,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            result = api_instance.get_node_by_fleet_id(FLEET_ID, NODE_ID)
            assert result.node_name == NODE_ID

    def test_get_node_by_fleet_id_error(self, api_instance):
        """404 when node does not exist in fleet."""
        mock_response = MockResponse(
            404,
            data=b'{"error": "not found"}',
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            with pytest.raises(ApiException) as exc_info:
                api_instance.get_node_by_fleet_id(FLEET_ID, NODE_ID)
            assert exc_info.value.status == 404

    # ------------------------------------------------------------------
    # list_nodes_by_fleet_id
    # ------------------------------------------------------------------

    def test_list_nodes_by_fleet_id_success(self, api_instance):
        """List nodes in a fleet."""
        body = {
            "nodes": [
                {"nodeName": NODE_ID, "state": "ACTIVE", "publicIp": "1.2.3.4", "fleetId": FLEET_ID},
            ],
        }
        mock_response = MockResponse(
            200,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            result = api_instance.list_nodes_by_fleet_id(FLEET_ID)
            assert isinstance(result, ListNodesResponse)

    def test_list_nodes_by_fleet_id_error(self, api_instance):
        """Error listing nodes."""
        mock_response = MockResponse(
            403,
            data=b'{"error": "forbidden"}',
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            with pytest.raises(ApiException) as exc_info:
                api_instance.list_nodes_by_fleet_id(FLEET_ID)
            assert exc_info.value.status == 403
