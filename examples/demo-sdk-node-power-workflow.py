"""
Voltage Park Cloud Platform — SDK Maintenance Workflow Demo

Demonstrates the full node maintenance lifecycle using the Voltage Park Python SDK:
    1. Baseline check (verify node is joined and schedulable)
    2. Pre-flight readiness (check if node is safe for power action)
    3. Cordon (mark node unschedulable)
    4. Drain (evict pods gracefully)
    5. Power action (ForceRestart)
    6. Poll until power operation completes
    7. Wait for node to rejoin the cluster
    8. Uncordon (mark node schedulable again)

Prerequisites:
    - Install the SDK:
        git clone https://github.com/voltagepark/vp-cloud-sdk.git
        cd vp-cloud-sdk && uv sync && source .venv/bin/activate

    - Set environment variables:
        export HOST="https://api.sea1.voltagepark.com"   # SEA1 region
        # or:  HOST="https://api.iad1.voltagepark.com"   # IAD1 region
        export CLIENT_ID="<your-client-id>"
        export CLIENT_SECRET="<your-client-secret>"

      Credentials are delivered securely through an encrypted channel.
      Request these credentials by connecting with Voltage Park Customer Service.
        export FLEET_ID="<your-fleet-id>"
        export NODE_ID="<your-node-id>"

    - The application principal must have customer-admin permissions
      for power operations.

Usage:
    python demo-sdk-maintenance-workflow.py
"""

import json
import os
import sys
import time
import uuid

import vpcloud_client
from vpcloud_client.models.mks2_drain_node_request import Mks2DrainNodeRequest
from vpcloud_client.models.node_power_operation import NodePowerOperation
from vpcloud_client.rest import ApiException

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

host = os.environ.get("HOST")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
fleet_id = os.environ.get("FLEET_ID")
node_id = os.environ.get("NODE_ID")

required = {"HOST": host, "CLIENT_ID": client_id, "CLIENT_SECRET": client_secret,
            "FLEET_ID": fleet_id, "NODE_ID": node_id}
missing = [k for k, v in required.items() if not v]
if missing:
    print(f"Error: missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

configuration = vpcloud_client.Configuration(
    host=host,
    client_id=client_id,
    client_secret=client_secret,
)

# Terminal statuses for power operations — stop polling when reached.
TERMINAL_STATUSES = {"SUCCESS", "FAILURE", "TIMED_OUT"}

# Polling intervals and timeouts (seconds).
DRAIN_POLL_INTERVAL = 5
DRAIN_TIMEOUT = 300
POWER_POLL_INTERVAL = 10
POWER_TIMEOUT = 300
REQUEST_TIMEOUT = 30  # per-request HTTP timeout for polling calls
REJOIN_POLL_INTERVAL = 10
REJOIN_TIMEOUT = 300


def show(obj):
    """Pretty-print any SDK response object as JSON."""
    print(json.dumps(obj.model_dump(mode="json", by_alias=True), indent=2, default=str))


def step(title):
    """Print a visible step header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------

with vpcloud_client.ApiClient(configuration) as api_client:
    # Each API class groups related endpoints by OpenAPI tag.
    #   - KubernetesApi:      cordon, uncordon, drain, list/get worker nodes
    #   - NodesApi:          power state (GET), node details (pre-flight readiness)
    #   - NodeOperationsApi: power operations (POST)
    kubernetes_api = vpcloud_client.KubernetesApi(api_client)
    nodes_api = vpcloud_client.NodesApi(api_client)
    operations_api = vpcloud_client.NodeOperationsApi(api_client)

    # ------------------------------------------------------------------
    # 1. Baseline — verify the node is joined and schedulable
    # ------------------------------------------------------------------
    step("1. Baseline — verify node state")

    node = kubernetes_api.get_customer_mks2_worker_node(fleet_id, node_id)
    print(f"  Node:               {node.id}")
    print(f"  Schedulable:        {node.schedulable}")
    print(f"  Drained:            {node.drained}")
    registration_status = getattr(
        node.registration_status, "value", node.registration_status
    )
    print(f"  RegistrationStatus: {registration_status}")

    if registration_status != "joined":
        print("\nError: Node has not joined the cluster. Cannot proceed.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 2. Pre-flight readiness — check if the node is safe for power action
    # ------------------------------------------------------------------
    step("2. Pre-flight readiness check")

    # This is advisory only and does not block power operations.
    # Display blockerMessage / warningMessage to the operator as-is.
    details = nodes_api.get_fleet_node_details(fleet_id, node_id)
    readiness = details.power_action_readiness
    print(f"  Ready:          {readiness.ready}")
    print(f"  BlockerMessage: {readiness.blocker_message}")
    print(f"  WarningMessage: {readiness.warning_message}")

    # ------------------------------------------------------------------
    # 3. Cordon — mark the node unschedulable
    # ------------------------------------------------------------------
    step("3. Cordon — mark node unschedulable")

    # Cordon prevents new pods from being scheduled on the node.
    # Existing pods continue running. Safe to call on an already-cordoned node.
    try:
        cordon_response = kubernetes_api.cordon_customer_mks2_worker_node(
            fleet_id,
            node_id,
            idempotency_key=str(uuid.uuid4()),
        )
        show(cordon_response)
    except ApiException as error:
        print(f"  Cordon failed: {error.status} — {error.body}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 4. Drain — evict pods gracefully
    # ------------------------------------------------------------------
    step("4. Drain — evict pods")

    # Drain also cordons automatically, so step 3 is optional.
    # PodDisruptionBudgets are respected.
    # The request body is optional; defaults are gracePeriodSeconds=30,
    # ignoreDaemonSets=true.
    try:
        drain_response = kubernetes_api.drain_customer_mks2_worker_node(
            fleet_id,
            node_id,
            idempotency_key=str(uuid.uuid4()),
            mks2_drain_node_request=Mks2DrainNodeRequest(
                grace_period_seconds=30,
                ignore_daemon_sets=True,
            ),
        )
        show(drain_response)
    except ApiException as error:
        print(f"  Drain failed: {error.status} — {error.body}")
        sys.exit(1)

    # 202 means eviction was initiated, not that the node is fully drained.
    # Poll until drained=true. This can take several minutes depending on
    # the number of pods, their grace period, and PodDisruptionBudgets.
    print("\n  Waiting for drain to complete...")
    drain_start = time.time()
    drain_succeeded = False
    while True:
        after_drain = kubernetes_api.get_customer_mks2_worker_node(
            fleet_id, node_id, _request_timeout=REQUEST_TIMEOUT,
        )
        if after_drain.drained:
            drain_succeeded = True
            break
        elapsed = time.time() - drain_start
        if elapsed >= DRAIN_TIMEOUT:
            print(f"\n  Drain timed out after {DRAIN_TIMEOUT}s.")
            print("  Node still has non-evicted pods (common on single-node clusters).")
            print("  Leaving node cordoned for operator intervention. Aborting workflow.")
            sys.exit(1)
        print(f"    drained={after_drain.drained}, retrying in {DRAIN_POLL_INTERVAL}s...")
        time.sleep(DRAIN_POLL_INTERVAL)
    print(f"  Drain complete: schedulable={after_drain.schedulable}, drained={after_drain.drained}")

    # ------------------------------------------------------------------
    # 5. Pre-flight readiness — confirm node is now ready
    # ------------------------------------------------------------------
    step("5. Pre-flight readiness (post-drain)")

    details = nodes_api.get_fleet_node_details(fleet_id, node_id)
    readiness = details.power_action_readiness
    print(f"  Ready:          {readiness.ready}")
    print(f"  BlockerMessage: {readiness.blocker_message}")
    print(f"  WarningMessage: {readiness.warning_message}")

    if not readiness.ready:
        print("\n  Warning: Node is not ready for power action. Proceeding anyway (advisory only).")

    # ------------------------------------------------------------------
    # 6. Power action — ForceRestart
    # ------------------------------------------------------------------
    step("6. Power action — ForceRestart")

    # Check current power state before queueing.
    current_power = nodes_api.get_node_power_state(fleet_id, node_id)
    print(f"  Current power state: {current_power.power_state}")

    # Queue the restart. All power operations require customer-admin role.
    # resetType values: On, ForceRestart, ForceOff, GracefulShutdown.
    try:
        queued = operations_api.create_node_power_operation(
            fleet_id,
            node_id,
            NodePowerOperation(reset_type="ForceRestart"),
            idempotency_key=str(uuid.uuid4()),
        )
        show(queued)
        print(f"\n  Operation queued: {queued.operation_id}")
    except ApiException as error:
        # Common power-specific errors:
        #   409 — transition conflicts with current state, or idempotency key in flight
        #   422 — idempotency key reused with a different body
        #   423 — another power operation already in progress
        #   502 — node BMC unreachable
        print(f"  Power operation failed: {error.status} — {error.body}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 7. Poll until the power operation reaches a terminal status
    # ------------------------------------------------------------------
    step("7. Polling power operation status")

    # Terminal statuses: SUCCESS, FAILURE, TIMED_OUT.
    # Non-terminal (keep polling): ACCEPTED, IN_PROGRESS.
    power_start = time.time()
    while True:
        state = nodes_api.get_node_power_state(
            fleet_id, node_id, _request_timeout=REQUEST_TIMEOUT,
        )
        if state.last_operation and state.last_operation.status in TERMINAL_STATUSES:
            break
        elapsed = time.time() - power_start
        if elapsed >= POWER_TIMEOUT:
            print(f"\n  Power poll timed out after {POWER_TIMEOUT}s.")
            print("  Leaving node cordoned for operator intervention. Aborting workflow.")
            sys.exit(1)
        operation_status = state.last_operation.status if state.last_operation else "unknown"
        print(f"    powerState={state.power_state}, operationStatus={operation_status}, retrying in {POWER_POLL_INTERVAL}s...")
        time.sleep(POWER_POLL_INTERVAL)

    last_op = state.last_operation
    print(f"  Power state:      {state.power_state}")
    print(f"  Operation status: {last_op.status if last_op else 'unknown'}")

    if not last_op or last_op.status != "SUCCESS":
        status = last_op.status if last_op else "unknown"
        print(f"\n  Error: Operation did not succeed. Status: {status}")
        if last_op and last_op.error:
            print(f"  Error detail: {last_op.error}")
        print("  Leaving node cordoned for operator intervention. Aborting workflow.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 8. Wait for node to rejoin the cluster
    # ------------------------------------------------------------------
    step("8. Waiting for node to rejoin the cluster")

    # After a power restart, the node needs time to boot and rejoin
    # Kubernetes. Uncordoning before the node is Ready can make it
    # schedulable while it cannot yet accept workloads.
    rejoin_start = time.time()
    while True:
        try:
            rejoined = kubernetes_api.get_customer_mks2_worker_node(
                fleet_id, node_id, _request_timeout=REQUEST_TIMEOUT,
            )
            reg = getattr(rejoined.registration_status, "value", rejoined.registration_status)
            if reg == "joined":
                print(f"  Node rejoined: registrationStatus={reg}")
                break
        except ApiException:
            pass  # node may be unreachable while rebooting
        elapsed = time.time() - rejoin_start
        if elapsed >= REJOIN_TIMEOUT:
            print(f"\n  Node did not rejoin within {REJOIN_TIMEOUT}s.")
            print("  Leaving node cordoned for operator intervention. Aborting workflow.")
            sys.exit(1)
        print(f"    Waiting for node to rejoin... ({int(elapsed)}s elapsed)")
        time.sleep(REJOIN_POLL_INTERVAL)

    # ------------------------------------------------------------------
    # 9. Uncordon — mark the node schedulable again
    # ------------------------------------------------------------------
    step("9. Uncordon — mark node schedulable")

    # Only uncordon after the node is back online and the power operation
    # completed successfully.
    try:
        uncordon_response = kubernetes_api.uncordon_customer_mks2_worker_node(
            fleet_id,
            node_id,
            idempotency_key=str(uuid.uuid4()),
        )
        show(uncordon_response)
    except ApiException as error:
        print(f"  Uncordon failed: {error.status} — {error.body}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 10. Final verification
    # ------------------------------------------------------------------
    step("10. Final verification")

    final_node = kubernetes_api.get_customer_mks2_worker_node(fleet_id, node_id)
    print(f"  Node:        {final_node.id}")
    print(f"  Schedulable: {final_node.schedulable}")
    print(f"  Drained:     {final_node.drained}")

    final_power = nodes_api.get_node_power_state(fleet_id, node_id)
    print(f"  Power state: {final_power.power_state}")

    print("\n  Maintenance workflow complete.")
