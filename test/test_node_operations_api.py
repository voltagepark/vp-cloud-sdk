# coding: utf-8

"""
    Voltage Park Cloud API — NodeOperationsApi unit tests.

    Tests the SDK client layer for power operations and node remediation.
    All HTTP calls are mocked so no real API traffic is generated.
"""

import json
import uuid

import pytest
from unittest.mock import patch

from vpcloud_client.api.node_operations_api import NodeOperationsApi
from vpcloud_client.models.node_power_operation import NodePowerOperation
from vpcloud_client.models.node_power_operation_queued import NodePowerOperationQueued
from vpcloud_client.models.remediate_node_request import RemediateNodeRequest
from vpcloud_client.models.remediate_node_response import RemediateNodeResponse
from vpcloud_client.rest import ApiException
from vpcloud_client import ApiClient
from test.utils import create_test_config, MockResponse

FLEET_ID = "00000000-0000-0000-0000-000000000001"
NODE_ID = "node-abc-123"


class TestNodeOperationsApi:
    """NodeOperationsApi unit tests"""

    @pytest.fixture
    def api_instance(self):
        """Create API instance for testing."""
        config = create_test_config()
        return NodeOperationsApi(api_client=ApiClient(config))

    # ------------------------------------------------------------------
    # create_node_power_operation
    # ------------------------------------------------------------------

    def test_create_node_power_operation_success(self, api_instance):
        """Queue a power operation and receive an ACCEPTED response."""
        body = {
            "nodeId": NODE_ID,
            "resetType": "ForceRestart",
            "powerStateBefore": "On",
            "status": "ACCEPTED",
            "operationId": "op-1111",
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
            result = api_instance.create_node_power_operation(
                FLEET_ID, NODE_ID, str(uuid.uuid4()),
                NodePowerOperation(reset_type="ForceRestart"),
            )
            assert isinstance(result, NodePowerOperationQueued)
            assert result.operation_id == "op-1111"
            assert result.reset_type == "ForceRestart"
            assert result.status == "ACCEPTED"

    def test_create_node_power_operation_409_conflict(self, api_instance):
        """409 when another operation with the same idempotency key is in flight."""
        mock_response = MockResponse(
            409,
            data=b'{"error": "Conflict: idempotency key in flight"}',
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            with pytest.raises(ApiException) as exc_info:
                api_instance.create_node_power_operation(
                    FLEET_ID, NODE_ID, str(uuid.uuid4()),
                    NodePowerOperation(reset_type="ForceRestart"),
                )
            assert exc_info.value.status == 409

    def test_create_node_power_operation_422_body_mismatch(self, api_instance):
        """422 when idempotency key reused with a different body."""
        mock_response = MockResponse(
            422,
            data=b'{"error": "Unprocessable Entity: body mismatch"}',
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            with pytest.raises(ApiException) as exc_info:
                api_instance.create_node_power_operation(
                    FLEET_ID, NODE_ID, str(uuid.uuid4()),
                    NodePowerOperation(reset_type="ForceOff"),
                )
            assert exc_info.value.status == 422

    def test_create_node_power_operation_423_locked(self, api_instance):
        """423 when another power operation is already in progress."""
        mock_response = MockResponse(
            423,
            data=b'{"error": "Locked: power operation in progress"}',
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            with pytest.raises(ApiException) as exc_info:
                api_instance.create_node_power_operation(
                    FLEET_ID, NODE_ID, str(uuid.uuid4()),
                    NodePowerOperation(reset_type="ForceRestart"),
                )
            assert exc_info.value.status == 423

    def test_create_node_power_operation_502_bmc_unreachable(self, api_instance):
        """502 when node BMC is unreachable."""
        mock_response = MockResponse(
            502,
            data=b'{"error": "Bad Gateway: BMC unreachable"}',
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            with pytest.raises(ApiException) as exc_info:
                api_instance.create_node_power_operation(
                    FLEET_ID, NODE_ID, str(uuid.uuid4()),
                    NodePowerOperation(reset_type="ForceRestart"),
                )
            assert exc_info.value.status == 502

    def test_create_node_power_operation_all_reset_types(self, api_instance):
        """All valid reset types should be accepted by the model."""
        for reset_type in ("On", "ForceOff", "GracefulShutdown", "ForceRestart"):
            body = {
                "nodeId": NODE_ID,
                "resetType": reset_type,
                "powerStateBefore": "On",
                "status": "ACCEPTED",
                "operationId": f"op-{reset_type}",
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
                result = api_instance.create_node_power_operation(
                    FLEET_ID, NODE_ID, str(uuid.uuid4()),
                    NodePowerOperation(reset_type=reset_type),
                )
                assert result.reset_type == reset_type

    # ------------------------------------------------------------------
    # remediate_nodes
    # ------------------------------------------------------------------

    def test_remediate_nodes_success(self, api_instance):
        """Successful remediation request."""
        body = [
            {"nodeId": NODE_ID, "remediateStatus": "ACCEPTED"},
        ]
        mock_response = MockResponse(
            200,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            result = api_instance.remediate_nodes(
                FLEET_ID,
                remediate_node_request=[
                    RemediateNodeRequest(
                        node_id=NODE_ID,
                        message="GPU unresponsive",
                        cause="hardware_failure",
                    ),
                ],
            )
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0].node_id == NODE_ID

    def test_remediate_nodes_error(self, api_instance):
        """Error on remediation request."""
        mock_response = MockResponse(
            400,
            data=b'{"error": "bad request"}',
            headers={"Content-Type": "application/json"},
        )
        with patch.object(
            api_instance.api_client.rest_client, "request",
            return_value=mock_response,
        ):
            with pytest.raises(ApiException) as exc_info:
                api_instance.remediate_nodes(
                    FLEET_ID,
                    remediate_node_request=[
                        RemediateNodeRequest(
                            node_id=NODE_ID,
                            message="GPU unresponsive",
                            cause="hardware_failure",
                        ),
                    ],
                )
            assert exc_info.value.status == 400
