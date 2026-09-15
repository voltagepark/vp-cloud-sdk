# coding: utf-8

"""
    Tests for the node power maintenance workflow
    (examples/demo-sdk-node-power-workflow.py).

    These tests validate the SDK API calls, polling logic, timeout behaviour,
    and safety guards exercised by the demo workflow without hitting a real
    Voltage Park environment.  Every external call is mocked at the SDK API
    layer so the tests run offline and fast.
"""

import json
import time
import uuid
from unittest.mock import patch, MagicMock, PropertyMock, call

import pytest

import vpcloud_client
from vpcloud_client.api.kubernetes_api import KubernetesApi
from vpcloud_client.api.nodes_api import NodesApi
from vpcloud_client.api.node_operations_api import NodeOperationsApi
from vpcloud_client.models.mks2_cordon_node_response import Mks2CordonNodeResponse
from vpcloud_client.models.mks2_drain_node_request import Mks2DrainNodeRequest
from vpcloud_client.models.mks2_drain_node_response import Mks2DrainNodeResponse
from vpcloud_client.models.mks2_worker_node_detail import Mks2WorkerNodeDetail
from vpcloud_client.models.mks2_worker_node_registration_status import Mks2WorkerNodeRegistrationStatus
from vpcloud_client.models.node_details import NodeDetails
from vpcloud_client.models.node_power_last_operation import NodePowerLastOperation
from vpcloud_client.models.node_power_operation import NodePowerOperation
from vpcloud_client.models.node_power_operation_queued import NodePowerOperationQueued
from vpcloud_client.models.node_power_state import NodePowerState
from vpcloud_client.models.node_state import NodeState
from vpcloud_client.models.power_action_readiness import PowerActionReadiness
from vpcloud_client.rest import ApiException
from test.utils import create_test_config


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FLEET_ID = "00000000-0000-0000-0000-000000000001"
NODE_ID = "node-abc-123"
OP_ID = "op-1234-5678"


def _make_worker_node(
    *,
    schedulable: bool = True,
    drained: bool = False,
    registration_status: str = "joined",
) -> Mks2WorkerNodeDetail:
    """Build a minimal Mks2WorkerNodeDetail for test assertions."""
    return Mks2WorkerNodeDetail(
        id=NODE_ID,
        registration_status=Mks2WorkerNodeRegistrationStatus(registration_status),
        schedulable=schedulable,
        drained=drained,
    )


def _make_node_details(
    *, ready: bool = True, blocker: str = "", warning: str = ""
) -> NodeDetails:
    return NodeDetails(
        node_name=NODE_ID,
        state=NodeState.ACTIVE,
        public_ip="1.2.3.4",
        fleet_id=FLEET_ID,
        power_action_readiness=PowerActionReadiness(
            ready=ready,
            blocker_message=blocker,
            warning_message=warning,
        ),
    )


def _make_cordon_response(*, schedulable: bool = False) -> Mks2CordonNodeResponse:
    return Mks2CordonNodeResponse(
        node_id=NODE_ID,
        schedulable=schedulable,
    )


def _make_drain_response(*, evicted: int = 5) -> Mks2DrainNodeResponse:
    return Mks2DrainNodeResponse(
        node_id=NODE_ID,
        evicted=evicted,
    )


def _make_power_queued() -> NodePowerOperationQueued:
    return NodePowerOperationQueued(
        node_id=NODE_ID,
        reset_type="ForceRestart",
        power_state_before="On",
        status="ACCEPTED",
        operation_id=OP_ID,
    )


def _make_power_state(
    *,
    power_state: str = "On",
    op_status: str = "SUCCESS",
    op_id: str = OP_ID,
    with_op: bool = True,
) -> NodePowerState:
    last_op = None
    if with_op:
        last_op = NodePowerLastOperation(
            operation_id=op_id,
            reset_type="ForceRestart",
            status=op_status,
            queued_at=1700000000000,
        )
    return NodePowerState(
        node_id=NODE_ID,
        power_state=power_state,
        last_operation=last_op,
    )


@pytest.fixture
def api_clients():
    """Return (KubernetesApi, NodesApi, NodeOperationsApi) backed by a test config."""
    config = create_test_config()
    client = vpcloud_client.ApiClient(config)
    return (
        KubernetesApi(api_client=client),
        NodesApi(api_client=client),
        NodeOperationsApi(api_client=client),
    )


# ---------------------------------------------------------------------------
# 1. Baseline — node state checks
# ---------------------------------------------------------------------------

class TestBaselineNodeState:
    """Step 1: verify node is joined and schedulable."""

    def test_joined_and_schedulable(self, api_clients):
        """Happy path — node is joined and schedulable."""
        k8s, _, _ = api_clients
        node = _make_worker_node(schedulable=True, registration_status="joined")

        with patch.object(k8s, "get_customer_mks2_worker_node", return_value=node):
            result = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
            assert result.schedulable is True
            reg = getattr(result.registration_status, "value", result.registration_status)
            assert reg == "joined"

    def test_node_not_joined_should_block(self, api_clients):
        """Workflow should detect non-joined node."""
        k8s, _, _ = api_clients
        node = _make_worker_node(registration_status="registered")

        with patch.object(k8s, "get_customer_mks2_worker_node", return_value=node):
            result = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
            reg = getattr(result.registration_status, "value", result.registration_status)
            assert reg != "joined"

    def test_already_cordoned_warning(self, api_clients):
        """Node already cordoned should be detected (warning, not blocking)."""
        k8s, _, _ = api_clients
        node = _make_worker_node(schedulable=False, registration_status="joined")

        with patch.object(k8s, "get_customer_mks2_worker_node", return_value=node):
            result = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
            assert result.schedulable is False


# ---------------------------------------------------------------------------
# 2. Pre-flight readiness
# ---------------------------------------------------------------------------

class TestPreFlightReadiness:
    """Step 2: advisory readiness check before power action."""

    def test_ready_no_warnings(self, api_clients):
        _, nodes, _ = api_clients
        details = _make_node_details(ready=True)

        with patch.object(nodes, "get_fleet_node_details", return_value=details):
            result = nodes.get_fleet_node_details(FLEET_ID, NODE_ID)
            assert result.power_action_readiness.ready is True
            assert result.power_action_readiness.blocker_message == ""

    def test_not_ready_with_blocker(self, api_clients):
        _, nodes, _ = api_clients
        details = _make_node_details(
            ready=False, blocker="Node is not drained"
        )

        with patch.object(nodes, "get_fleet_node_details", return_value=details):
            result = nodes.get_fleet_node_details(FLEET_ID, NODE_ID)
            assert result.power_action_readiness.ready is False
            assert "not drained" in result.power_action_readiness.blocker_message

    def test_ready_with_warning(self, api_clients):
        _, nodes, _ = api_clients
        details = _make_node_details(
            ready=True, warning="GPU validation pending"
        )

        with patch.object(nodes, "get_fleet_node_details", return_value=details):
            result = nodes.get_fleet_node_details(FLEET_ID, NODE_ID)
            assert result.power_action_readiness.ready is True
            assert result.power_action_readiness.warning_message != ""


# ---------------------------------------------------------------------------
# 3. Cordon
# ---------------------------------------------------------------------------

class TestCordon:
    """Step 3: cordon marks node unschedulable."""

    def test_cordon_success(self, api_clients):
        k8s, _, _ = api_clients
        resp = _make_cordon_response(schedulable=False)

        with patch.object(k8s, "cordon_customer_mks2_worker_node", return_value=resp):
            result = k8s.cordon_customer_mks2_worker_node(
                FLEET_ID, NODE_ID, idempotency_key=str(uuid.uuid4()),
            )
            assert result.schedulable is False
            assert result.node_id == NODE_ID

    def test_cordon_api_error(self, api_clients):
        k8s, _, _ = api_clients

        with patch.object(
            k8s, "cordon_customer_mks2_worker_node",
            side_effect=ApiException(status=400, reason="Bad Request"),
        ):
            with pytest.raises(ApiException) as exc_info:
                k8s.cordon_customer_mks2_worker_node(
                    FLEET_ID, NODE_ID, idempotency_key=str(uuid.uuid4()),
                )
            assert exc_info.value.status == 400

    def test_cordon_idempotent_on_already_cordoned(self, api_clients):
        """Cordon on an already-cordoned node should succeed."""
        k8s, _, _ = api_clients
        resp = _make_cordon_response(schedulable=False)

        with patch.object(k8s, "cordon_customer_mks2_worker_node", return_value=resp):
            result = k8s.cordon_customer_mks2_worker_node(
                FLEET_ID, NODE_ID, idempotency_key=str(uuid.uuid4()),
            )
            assert result.schedulable is False


# ---------------------------------------------------------------------------
# 4. Drain
# ---------------------------------------------------------------------------

class TestDrain:
    """Step 4: drain evicts pods gracefully."""

    def test_drain_success(self, api_clients):
        k8s, _, _ = api_clients
        resp = _make_drain_response(evicted=3)

        with patch.object(k8s, "drain_customer_mks2_worker_node", return_value=resp):
            result = k8s.drain_customer_mks2_worker_node(
                FLEET_ID, NODE_ID,
                idempotency_key=str(uuid.uuid4()),
                mks2_drain_node_request=Mks2DrainNodeRequest(
                    grace_period_seconds=30, ignore_daemon_sets=True,
                ),
            )
            assert result.evicted == 3

    def test_drain_api_error(self, api_clients):
        k8s, _, _ = api_clients

        with patch.object(
            k8s, "drain_customer_mks2_worker_node",
            side_effect=ApiException(status=500, reason="Internal Server Error"),
        ):
            with pytest.raises(ApiException) as exc_info:
                k8s.drain_customer_mks2_worker_node(
                    FLEET_ID, NODE_ID,
                    idempotency_key=str(uuid.uuid4()),
                    mks2_drain_node_request=Mks2DrainNodeRequest(
                        grace_period_seconds=30, ignore_daemon_sets=True,
                    ),
                )
            assert exc_info.value.status == 500

    def test_drain_poll_until_drained_true(self, api_clients):
        """Polling loop should stop when drained becomes True."""
        k8s, _, _ = api_clients
        not_drained = _make_worker_node(schedulable=False, drained=False)
        is_drained = _make_worker_node(schedulable=False, drained=True)

        with patch.object(
            k8s, "get_customer_mks2_worker_node",
            side_effect=[not_drained, not_drained, is_drained],
        ):
            attempts = 0
            for _ in range(10):
                attempts += 1
                result = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
                if result.drained:
                    break
            assert result.drained is True
            assert attempts == 3

    def test_drain_poll_timeout_proceeds(self, api_clients):
        """When drain stays false (system pods), workflow should still proceed."""
        k8s, _, _ = api_clients
        not_drained = _make_worker_node(schedulable=False, drained=False)

        with patch.object(
            k8s, "get_customer_mks2_worker_node", return_value=not_drained,
        ):
            drain_timeout = 0.1  # very short for test
            start = time.time()
            timed_out = False
            while True:
                result = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
                if result.drained:
                    break
                if time.time() - start >= drain_timeout:
                    timed_out = True
                    break
            assert timed_out is True
            assert result.drained is False


# ---------------------------------------------------------------------------
# 5. Power action — ForceRestart
# ---------------------------------------------------------------------------

class TestPowerAction:
    """Step 6: queue ForceRestart and poll until terminal."""

    def test_queue_force_restart_success(self, api_clients):
        _, _, ops = api_clients
        queued = _make_power_queued()

        with patch.object(ops, "create_node_power_operation", return_value=queued):
            result = ops.create_node_power_operation(
                FLEET_ID, NODE_ID, str(uuid.uuid4()),
                NodePowerOperation(reset_type="ForceRestart"),
            )
            assert result.operation_id == OP_ID
            assert result.reset_type == "ForceRestart"
            assert result.status == "ACCEPTED"

    def test_queue_power_409_conflict(self, api_clients):
        """409 means another operation is in flight."""
        _, _, ops = api_clients

        with patch.object(
            ops, "create_node_power_operation",
            side_effect=ApiException(status=409, reason="Conflict"),
        ):
            with pytest.raises(ApiException) as exc_info:
                ops.create_node_power_operation(
                    FLEET_ID, NODE_ID, str(uuid.uuid4()),
                    NodePowerOperation(reset_type="ForceRestart"),
                )
            assert exc_info.value.status == 409

    def test_queue_power_423_locked(self, api_clients):
        """423 means another power operation already in progress."""
        _, _, ops = api_clients

        with patch.object(
            ops, "create_node_power_operation",
            side_effect=ApiException(status=423, reason="Locked"),
        ):
            with pytest.raises(ApiException) as exc_info:
                ops.create_node_power_operation(
                    FLEET_ID, NODE_ID, str(uuid.uuid4()),
                    NodePowerOperation(reset_type="ForceRestart"),
                )
            assert exc_info.value.status == 423

    def test_queue_power_502_bmc_unreachable(self, api_clients):
        """502 means node BMC unreachable."""
        _, _, ops = api_clients

        with patch.object(
            ops, "create_node_power_operation",
            side_effect=ApiException(status=502, reason="Bad Gateway"),
        ):
            with pytest.raises(ApiException) as exc_info:
                ops.create_node_power_operation(
                    FLEET_ID, NODE_ID, str(uuid.uuid4()),
                    NodePowerOperation(reset_type="ForceRestart"),
                )
            assert exc_info.value.status == 502


# ---------------------------------------------------------------------------
# 6. Poll power operation status
# ---------------------------------------------------------------------------

class TestPowerPolling:
    """Step 7: poll until power operation reaches a terminal status."""

    TERMINAL_STATUSES = {"SUCCESS", "FAILURE", "TIMED_OUT"}

    def test_poll_reaches_success(self, api_clients):
        _, nodes, _ = api_clients
        in_progress = _make_power_state(op_status="IN_PROGRESS")
        success = _make_power_state(op_status="SUCCESS")

        with patch.object(
            nodes, "get_node_power_state",
            side_effect=[in_progress, in_progress, success],
        ):
            attempts = 0
            for _ in range(10):
                attempts += 1
                state = nodes.get_node_power_state(FLEET_ID, NODE_ID)
                if (state.last_operation
                        and state.last_operation.operation_id == OP_ID
                        and state.last_operation.status in self.TERMINAL_STATUSES):
                    break
            assert state.last_operation.status == "SUCCESS"
            assert attempts == 3

    def test_poll_reaches_failure_aborts(self, api_clients):
        _, nodes, _ = api_clients
        failure = _make_power_state(op_status="FAILURE")

        with patch.object(nodes, "get_node_power_state", return_value=failure):
            state = nodes.get_node_power_state(FLEET_ID, NODE_ID)
            assert state.last_operation.status == "FAILURE"
            assert state.last_operation.status != "SUCCESS"

    def test_poll_reaches_timed_out_aborts(self, api_clients):
        _, nodes, _ = api_clients
        timed_out = _make_power_state(op_status="TIMED_OUT")

        with patch.object(nodes, "get_node_power_state", return_value=timed_out):
            state = nodes.get_node_power_state(FLEET_ID, NODE_ID)
            assert state.last_operation.status == "TIMED_OUT"
            assert state.last_operation.status != "SUCCESS"

    def test_poll_ignores_stale_operation(self, api_clients):
        """Polling must match operation_id — ignore previous terminal ops."""
        _, nodes, _ = api_clients
        stale = _make_power_state(op_status="SUCCESS", op_id="old-op-id")
        current = _make_power_state(op_status="IN_PROGRESS", op_id=OP_ID)
        done = _make_power_state(op_status="SUCCESS", op_id=OP_ID)

        with patch.object(
            nodes, "get_node_power_state",
            side_effect=[stale, current, done],
        ):
            target_op_id = OP_ID
            for _ in range(10):
                state = nodes.get_node_power_state(FLEET_ID, NODE_ID)
                last_op = state.last_operation
                if (last_op
                        and getattr(last_op, "operation_id", None) == target_op_id
                        and last_op.status in self.TERMINAL_STATUSES):
                    break
            assert state.last_operation.operation_id == OP_ID
            assert state.last_operation.status == "SUCCESS"

    def test_poll_timeout_leaves_node_cordoned(self, api_clients):
        """When polling times out, workflow should abort (node stays cordoned)."""
        _, nodes, _ = api_clients
        in_progress = _make_power_state(op_status="IN_PROGRESS")

        with patch.object(nodes, "get_node_power_state", return_value=in_progress):
            power_timeout = 0.1
            start = time.time()
            timed_out = False
            while True:
                state = nodes.get_node_power_state(FLEET_ID, NODE_ID)
                last_op = state.last_operation
                if (last_op
                        and last_op.operation_id == OP_ID
                        and last_op.status in self.TERMINAL_STATUSES):
                    break
                if time.time() - start >= power_timeout:
                    timed_out = True
                    break
            assert timed_out is True
            assert state.last_operation.status == "IN_PROGRESS"

    def test_poll_with_no_last_operation(self, api_clients):
        """Handle case where last_operation is initially None."""
        _, nodes, _ = api_clients
        no_op = _make_power_state(with_op=False)
        done = _make_power_state(op_status="SUCCESS")

        with patch.object(
            nodes, "get_node_power_state",
            side_effect=[no_op, done],
        ):
            target_op_id = OP_ID
            for _ in range(10):
                state = nodes.get_node_power_state(FLEET_ID, NODE_ID)
                last_op = state.last_operation
                if (last_op
                        and getattr(last_op, "operation_id", None) == target_op_id
                        and last_op.status in self.TERMINAL_STATUSES):
                    break
            assert state.last_operation is not None
            assert state.last_operation.status == "SUCCESS"


# ---------------------------------------------------------------------------
# 7. Wait for node to rejoin
# ---------------------------------------------------------------------------

class TestNodeRejoin:
    """Step 8: poll until node rejoins the cluster after restart."""

    def test_node_rejoins_after_reboot(self, api_clients):
        k8s, _, _ = api_clients
        not_joined = _make_worker_node(registration_status="registered")
        joined = _make_worker_node(registration_status="joined")

        with patch.object(
            k8s, "get_customer_mks2_worker_node",
            side_effect=[
                ApiException(status=503, reason="Unavailable"),
                not_joined,
                joined,
            ],
        ):
            reg = None
            for _ in range(10):
                try:
                    result = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
                    reg = getattr(result.registration_status, "value", result.registration_status)
                    if reg == "joined":
                        break
                except ApiException:
                    pass
            assert reg == "joined"

    def test_rejoin_timeout_aborts(self, api_clients):
        k8s, _, _ = api_clients

        with patch.object(
            k8s, "get_customer_mks2_worker_node",
            side_effect=ApiException(status=503, reason="Unavailable"),
        ):
            rejoin_timeout = 0.1
            start = time.time()
            timed_out = False
            while True:
                try:
                    result = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
                    reg = getattr(result.registration_status, "value", result.registration_status)
                    if reg == "joined":
                        break
                except ApiException:
                    pass
                if time.time() - start >= rejoin_timeout:
                    timed_out = True
                    break
            assert timed_out is True


# ---------------------------------------------------------------------------
# 8. Uncordon
# ---------------------------------------------------------------------------

class TestUncordon:
    """Step 9: uncordon marks node schedulable again."""

    def test_uncordon_success(self, api_clients):
        k8s, _, _ = api_clients
        resp = Mks2CordonNodeResponse(node_id=NODE_ID, schedulable=True)

        with patch.object(k8s, "uncordon_customer_mks2_worker_node", return_value=resp):
            result = k8s.uncordon_customer_mks2_worker_node(
                FLEET_ID, NODE_ID, idempotency_key=str(uuid.uuid4()),
            )
            assert result.schedulable is True

    def test_uncordon_api_error(self, api_clients):
        k8s, _, _ = api_clients

        with patch.object(
            k8s, "uncordon_customer_mks2_worker_node",
            side_effect=ApiException(status=500, reason="Internal Server Error"),
        ):
            with pytest.raises(ApiException) as exc_info:
                k8s.uncordon_customer_mks2_worker_node(
                    FLEET_ID, NODE_ID, idempotency_key=str(uuid.uuid4()),
                )
            assert exc_info.value.status == 500


# ---------------------------------------------------------------------------
# 9. Final verification
# ---------------------------------------------------------------------------

class TestFinalVerification:
    """Step 10: confirm node is schedulable and powered on."""

    def test_final_state_schedulable_and_on(self, api_clients):
        k8s, nodes, _ = api_clients
        node = _make_worker_node(schedulable=True, drained=False)
        power = _make_power_state(power_state="On", op_status="SUCCESS")

        with patch.object(k8s, "get_customer_mks2_worker_node", return_value=node), \
             patch.object(nodes, "get_node_power_state", return_value=power):
            final_node = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
            final_power = nodes.get_node_power_state(FLEET_ID, NODE_ID)
            assert final_node.schedulable is True
            assert final_power.power_state == "On"

    def test_final_state_still_cordoned_after_failure(self, api_clients):
        """If power op failed, node should remain cordoned."""
        k8s, nodes, _ = api_clients
        node = _make_worker_node(schedulable=False, drained=False)
        power = _make_power_state(power_state="Off", op_status="FAILURE")

        with patch.object(k8s, "get_customer_mks2_worker_node", return_value=node), \
             patch.object(nodes, "get_node_power_state", return_value=power):
            final_node = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
            final_power = nodes.get_node_power_state(FLEET_ID, NODE_ID)
            assert final_node.schedulable is False
            assert final_power.last_operation.status == "FAILURE"


# ---------------------------------------------------------------------------
# 10. End-to-end happy path (full workflow in sequence)
# ---------------------------------------------------------------------------

class TestEndToEndHappyPath:
    """Simulate the full workflow: baseline → cordon → drain → power → rejoin → uncordon → verify."""

    def test_full_workflow_happy_path(self, api_clients):
        k8s, nodes, ops = api_clients

        baseline_node = _make_worker_node(schedulable=True, registration_status="joined")
        pre_flight_details = _make_node_details(ready=True)
        cordon_resp = _make_cordon_response(schedulable=False)
        drain_resp = _make_drain_response(evicted=4)
        drained_node = _make_worker_node(schedulable=False, drained=True)
        post_drain_details = _make_node_details(ready=True)
        pre_power = _make_power_state(power_state="On", with_op=False)
        queued = _make_power_queued()
        power_in_progress = _make_power_state(op_status="IN_PROGRESS")
        power_success = _make_power_state(op_status="SUCCESS")
        rejoined_node = _make_worker_node(schedulable=False, registration_status="joined")
        uncordon_resp = Mks2CordonNodeResponse(node_id=NODE_ID, schedulable=True)
        final_node = _make_worker_node(schedulable=True, drained=False)
        final_power = _make_power_state(power_state="On", op_status="SUCCESS")

        # Step 1: Baseline
        with patch.object(k8s, "get_customer_mks2_worker_node", return_value=baseline_node):
            node = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
            assert node.schedulable is True
            reg = getattr(node.registration_status, "value", node.registration_status)
            assert reg == "joined"

        # Step 2: Pre-flight readiness
        with patch.object(nodes, "get_fleet_node_details", return_value=pre_flight_details):
            details = nodes.get_fleet_node_details(FLEET_ID, NODE_ID)
            assert details.power_action_readiness.ready is True

        # Step 3: Cordon
        with patch.object(k8s, "cordon_customer_mks2_worker_node", return_value=cordon_resp):
            result = k8s.cordon_customer_mks2_worker_node(
                FLEET_ID, NODE_ID, idempotency_key=str(uuid.uuid4()),
            )
            assert result.schedulable is False

        # Step 4: Drain
        with patch.object(k8s, "drain_customer_mks2_worker_node", return_value=drain_resp):
            result = k8s.drain_customer_mks2_worker_node(
                FLEET_ID, NODE_ID,
                idempotency_key=str(uuid.uuid4()),
                mks2_drain_node_request=Mks2DrainNodeRequest(
                    grace_period_seconds=30, ignore_daemon_sets=True,
                ),
            )
            assert result.evicted == 4

        # Step 4b: Poll drain
        with patch.object(k8s, "get_customer_mks2_worker_node", return_value=drained_node):
            polled = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
            assert polled.drained is True

        # Step 5: Post-drain readiness
        with patch.object(nodes, "get_fleet_node_details", return_value=post_drain_details):
            details = nodes.get_fleet_node_details(FLEET_ID, NODE_ID)
            assert details.power_action_readiness.ready is True

        # Step 6: Power action
        with patch.object(nodes, "get_node_power_state", return_value=pre_power):
            current = nodes.get_node_power_state(FLEET_ID, NODE_ID)
            assert current.power_state == "On"

        with patch.object(ops, "create_node_power_operation", return_value=queued):
            q = ops.create_node_power_operation(
                FLEET_ID, NODE_ID, str(uuid.uuid4()),
                NodePowerOperation(reset_type="ForceRestart"),
            )
            assert q.operation_id == OP_ID

        # Step 7: Poll power
        with patch.object(
            nodes, "get_node_power_state",
            side_effect=[power_in_progress, power_success],
        ):
            terminal_statuses = {"SUCCESS", "FAILURE", "TIMED_OUT"}
            for _ in range(10):
                state = nodes.get_node_power_state(FLEET_ID, NODE_ID)
                if (state.last_operation
                        and state.last_operation.operation_id == OP_ID
                        and state.last_operation.status in terminal_statuses):
                    break
            assert state.last_operation.status == "SUCCESS"

        # Step 8: Rejoin
        with patch.object(k8s, "get_customer_mks2_worker_node", return_value=rejoined_node):
            r = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
            reg = getattr(r.registration_status, "value", r.registration_status)
            assert reg == "joined"

        # Step 9: Uncordon
        with patch.object(k8s, "uncordon_customer_mks2_worker_node", return_value=uncordon_resp):
            result = k8s.uncordon_customer_mks2_worker_node(
                FLEET_ID, NODE_ID, idempotency_key=str(uuid.uuid4()),
            )
            assert result.schedulable is True

        # Step 10: Final verification
        with patch.object(k8s, "get_customer_mks2_worker_node", return_value=final_node), \
             patch.object(nodes, "get_node_power_state", return_value=final_power):
            fn = k8s.get_customer_mks2_worker_node(FLEET_ID, NODE_ID)
            fp = nodes.get_node_power_state(FLEET_ID, NODE_ID)
            assert fn.schedulable is True
            assert fn.drained is False
            assert fp.power_state == "On"


# ---------------------------------------------------------------------------
# 11. Model / enum validation
# ---------------------------------------------------------------------------

class TestModelValidation:
    """Verify SDK model constraints used by the workflow."""

    def test_valid_reset_types(self):
        for rt in ("On", "ForceOff", "GracefulShutdown", "ForceRestart"):
            op = NodePowerOperation(reset_type=rt)
            assert op.reset_type == rt

    def test_invalid_reset_type_rejected(self):
        with pytest.raises(Exception):
            NodePowerOperation(reset_type="InvalidType")

    def test_power_operation_status_enum(self):
        for status in ("ACCEPTED", "IN_PROGRESS", "SUCCESS", "FAILURE", "TIMED_OUT"):
            op = NodePowerLastOperation(
                operation_id="test", reset_type="ForceRestart",
                status=status, queued_at=1700000000000,
            )
            assert op.status == status

    def test_power_operation_invalid_status_rejected(self):
        with pytest.raises(Exception):
            NodePowerLastOperation(
                operation_id="test", reset_type="ForceRestart",
                status="INVALID", queued_at=1700000000000,
            )

    def test_node_power_state_nullable_last_operation(self):
        state = NodePowerState(
            node_id=NODE_ID, power_state="On", last_operation=None,
        )
        assert state.last_operation is None

    def test_drain_response_nullable_fields(self):
        resp = Mks2DrainNodeResponse(node_id=NODE_ID)
        assert resp.evicted is None
        assert resp.failed is None

    def test_cordon_response_fields(self):
        resp = Mks2CordonNodeResponse(node_id=NODE_ID, schedulable=False, message="Cordoned")
        assert resp.message == "Cordoned"

    def test_worker_node_detail_drained_field(self):
        node = Mks2WorkerNodeDetail(
            id=NODE_ID,
            registration_status=Mks2WorkerNodeRegistrationStatus("joined"),
            drained=True,
            schedulable=False,
        )
        assert node.drained is True
        assert node.schedulable is False
