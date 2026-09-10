import asyncio
import time

from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.live import Live

from .node import KademliaNode
from .task_router import TaskRouter
from heartbeat_network import start_heartbeat, send_heartbeats


console = Console()


# ==========================================
# MESH CONFIGURATION
# ==========================================

NODE_CONFIG = [
    ("NODE1", 8500, 9500),
    ("NODE2", 8501, 9501),
    ("NODE3", 8502, 9502),
]


# ==========================================
# CREATE NODES
# ==========================================

nodes = {}

for name, port, gossip_port in NODE_CONFIG:

    nodes[name] = KademliaNode(
        host="127.0.0.1",
        port=port,
        gossip_port=gossip_port
    )


# ==========================================
# TASK ROUTER
# ==========================================

router = TaskRouter()

router.update_node_load("NODE1", 80, 70)
router.update_node_load("NODE2", 30, 40)
router.update_node_load("NODE3", 50, 50)


# ==========================================
# CONNECT PEERS
# ==========================================

for name, node in nodes.items():

    for other_name, other_node in nodes.items():

        if name != other_name:

            node.add_peer(
                other_node.node_id,
                other_node.host,
                other_node.port,
                other_node.gossip_port
            )


# ==========================================
# TASK STATE
# ==========================================

tasks = [
    {
        "task": "Task-1",
        "node": "NOT ASSIGNED",
        "status": "WAITING"
    }
]


# ==========================================
# HEARTBEAT STORAGE
# ==========================================

heartbeat_transports = {}
heartbeat_tasks = []
monitor_tasks = []


# ==========================================
# DASHBOARD
# ==========================================

def create_dashboard():

    # --------------------------------------
    # MESH TOPOLOGY
    # --------------------------------------

    node_table = Table(
        title="Mesh Topology"
    )

    node_table.add_column("Node")
    node_table.add_column("Discovery")
    node_table.add_column("Gossip")
    node_table.add_column("Heartbeat")
    node_table.add_column("Peers")
    node_table.add_column("Status")

    for name, node in nodes.items():

        active_peers = node.get_active_peers()

        # A node is considered active if:
        # it has active heartbeat peers.
        if len(active_peers) > 0:
            status = "ACTIVE"
        else:
            status = "WAITING"

        node_table.add_row(
            name,
            str(node.port),
            str(node.gossip_port),
            str(node.port + 2000),
            str(node.routing_table.count()),
            status
        )


    # --------------------------------------
    # TASK EXECUTION
    # --------------------------------------

    task_table = Table(
        title="Task Execution"
    )

    task_table.add_column("Task")
    task_table.add_column("Assigned Node")
    task_table.add_column("Status")

    for task in tasks:

        task_table.add_row(
            task["task"],
            task["node"],
            task["status"]
        )


    # --------------------------------------
    # TASK ROUTER
    # --------------------------------------

    router_table = Table(
        title="Task Router"
    )

    router_table.add_column("Node")
    router_table.add_column("CPU")
    router_table.add_column("RAM")
    router_table.add_column("Load")
    router_table.add_column("Active")

    for node_id, data in router.nodes.items():

        load = router.calculate_load(
            data["cpu"],
            data["ram"]
        )

        router_table.add_row(
            node_id,
            f"{data['cpu']}%",
            f"{data['ram']}%",
            f"{load:.1f}%",
            str(data["active"])
        )


    # --------------------------------------
    # DASHBOARD
    # --------------------------------------

    content = Group(
        node_table,
        task_table,
        router_table
    )

    return Panel(
        content,
        title="MESHWEAVER LIVE DASHBOARD"
    )


# ==========================================
# START HEARTBEAT SERVICES
# ==========================================

async def start_heartbeat_services():

    for name, node in nodes.items():

        transport = await start_heartbeat(node)

        heartbeat_transports[name] = transport

        print(
            f"[HEARTBEAT] {name} service started "
            f"on port {node.port + 2000}"
        )


    # Start heartbeat senders
    for name, node in nodes.items():

        task = asyncio.create_task(
            send_heartbeats(
                node,
                heartbeat_transports[name]
            )
        )

        heartbeat_tasks.append(task)


    # Start heartbeat monitors
    for name, node in nodes.items():

        task = asyncio.create_task(
            node.start_heartbeat_monitor()
        )

        monitor_tasks.append(task)


# ==========================================
# ASSIGN TASK
# ==========================================

def assign_task():

    result = router.route_task("Task-1")

    if result["success"]:

        tasks[0]["node"] = result["node"]
        tasks[0]["status"] = "RUNNING"

        print(
            f"[TASK] Task-1 assigned to "
            f"{result['node']}"
        )

    else:

        tasks[0]["status"] = "FAILED"

        print("[TASK] No active node available")


# ==========================================
# SIMULATE FAILURE
# ==========================================

def simulate_failure():

    failed_node = tasks[0]["node"]

    print()
    print("========================================")
    print("SIMULATING NODE FAILURE")
    print("========================================")
    print(f"Failed node: {failed_node}")

    # Stop heartbeat sender
    index = list(nodes.keys()).index(failed_node)

    heartbeat_tasks[index].cancel()

    # Mark failed node inactive
    router.mark_node_inactive(
        failed_node
    )

    print(
        f"[FAILURE] {failed_node} heartbeat stopped"
    )

    return failed_node


# ==========================================
# RE-ROUTE TASK
# ==========================================

def reroute_task(failed_node):

    print()
    print("========================================")
    print("TASK RE-ROUTING")
    print("========================================")

    result = router.reroute_task(
        "Task-1",
        failed_node
    )

    if result["success"]:

        tasks[0]["node"] = result["node"]
        tasks[0]["status"] = "RE-ROUTED"

        print(
            f"[ROUTER] Task-1 re-routed to "
            f"{result['node']}"
        )

    else:

        tasks[0]["status"] = "FAILED"

        print(
            "[ROUTER] No active node available"
        )


# ==========================================
# MAIN
# ==========================================

async def main():

    print("========================================")
    print("MESHWEAVER WEEK 4")
    print("PERSON 3 - LIVE DASHBOARD")
    print("========================================")

    await start_heartbeat_services()

    await asyncio.sleep(3)

    # Assign task
    assign_task()

    # Show normal operation
    with Live(
        create_dashboard(),
        refresh_per_second=2,
        console=console
    ) as live:

        # Normal operation
        for _ in range(8):

            live.update(
                create_dashboard()
            )

            await asyncio.sleep(1)


        # Simulate failure
        failed_node = simulate_failure()

        # Wait for heartbeat timeout
        print()
        print(
            "Waiting for heartbeat failure detection..."
        )

        for _ in range(12):

            live.update(
                create_dashboard()
            )

            await asyncio.sleep(1)


        # Re-route
        reroute_task(failed_node)

        # Show final dashboard
        for _ in range(5):

            live.update(
                create_dashboard()
            )

            await asyncio.sleep(1)


    # ======================================
    # CLEANUP
    # ======================================

    for task in heartbeat_tasks:
        task.cancel()

    for task in monitor_tasks:
        task.cancel()

    for transport in heartbeat_transports.values():
        transport.close()

    print()
    print("========================================")
    print("WEEK 4 DASHBOARD INTEGRATION COMPLETE")
    print("========================================")


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:

        print("\nDashboard stopped.")
