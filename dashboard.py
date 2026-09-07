import time

from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.live import Live

from node import KademliaNode
from task_router import TaskRouter


console = Console()


# ==========================================
# CREATE MESHWEAVER NODES
# ==========================================

nodes = {
    "NODE1": KademliaNode(
        host="127.0.0.1",
        port=8000,
        gossip_port=9000
    ),

    "NODE2": KademliaNode(
        host="127.0.0.1",
        port=8001,
        gossip_port=9001
    ),

    "NODE3": KademliaNode(
        host="127.0.0.1",
        port=8002,
        gossip_port=9002
    )
}


# ==========================================
# CREATE TASK ROUTER
# ==========================================

router = TaskRouter()


# Add node load information
router.update_node_load("NODE1", 25, 40)
router.update_node_load("NODE2", 60, 55)
router.update_node_load("NODE3", 90, 80)


# ==========================================
# CONNECT NODES USING ROUTING TABLE
# ==========================================

node_list = list(nodes.items())

for name, node in node_list:

    for other_name, other_node in node_list:

        if name != other_name:

            node.add_peer(
                other_node.node_id,
                other_node.host,
                other_node.port,
                other_node.gossip_port
            )


# ==========================================
# TASK INFORMATION
# ==========================================

tasks = [
    {
        "task": "Task-1",
        "node": "NODE1",
        "status": "COMPLETED"
    },

    {
        "task": "Task-2",
        "node": "NODE2",
        "status": "RUNNING"
    }
]


# ==========================================
# CREATE DASHBOARD
# ==========================================

def create_dashboard():

    # --------------------------------------
    # MESH TOPOLOGY TABLE
    # --------------------------------------

    node_table = Table(
        title="Mesh Topology"
    )

    node_table.add_column("Node ID")
    node_table.add_column("Discovery")
    node_table.add_column("Gossip")
    node_table.add_column("Peers")
    node_table.add_column("Status")

    for name, node in nodes.items():

        active_peers = node.get_active_peers()

        # Determine heartbeat status
        if len(active_peers) > 0:
            status = "ACTIVE"
        else:
            status = "WAITING"

        node_table.add_row(
            name,
            str(node.port),
            str(node.gossip_port),
            str(node.routing_table.count()),
            status
        )


    # --------------------------------------
    # TASK EXECUTION TABLE
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
    # TASK ROUTER TABLE
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
    # COMBINE ALL TABLES
    # --------------------------------------

    content = Group(
        node_table,
        task_table,
        router_table
    )


    # --------------------------------------
    # MAIN DASHBOARD PANEL
    # --------------------------------------

    return Panel(
        content,
        title="MESHWEAVER LIVE DASHBOARD"
    )


# ==========================================
# RUN DASHBOARD
# ==========================================

def main():

    print("Starting MeshWeaver Dashboard...")

    with Live(
        create_dashboard(),
        refresh_per_second=1,
        console=console
    ) as live:

        for _ in range(20):

            live.update(
                create_dashboard()
            )

            time.sleep(1)


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    main()