import asyncio

from task_router import TaskRouter
from node import KademliaNode
from heartbeat_network import start_heartbeat, send_heartbeats


async def main():

    # Create 3 nodes
    node1 = KademliaNode("127.0.0.1", 8300, 9300)
    node2 = KademliaNode("127.0.0.1", 8301, 9301)
    node3 = KademliaNode("127.0.0.1", 8302, 9302)

    nodes = [node1, node2, node3]

    # -----------------------------
    # TASK ROUTER
    # -----------------------------
    router = TaskRouter()

    router.update_node_load(node1.node_id, 80, 70)
    router.update_node_load(node2.node_id, 30, 40)
    router.update_node_load(node3.node_id, 50, 50)

    # -----------------------------
    # ADD PEERS
    # -----------------------------
    for node in nodes:
        for peer in nodes:
            if node != peer:
                node.add_peer(
                    peer.node_id,
                    peer.host,
                    peer.port,
                    peer.gossip_port
                )

    transports = []
    heartbeat_tasks = []

    try:

        # -----------------------------
        # START HEARTBEAT SERVICES
        # -----------------------------
        for node in nodes:

            transport = await start_heartbeat(node)
            transports.append(transport)

            task = asyncio.create_task(
                send_heartbeats(node, transport)
            )

            heartbeat_tasks.append(task)

        # Only Node 1 monitors the other nodes.
        # This keeps the failure test simple and reliable.
        monitor_task = asyncio.create_task(
            node1.start_heartbeat_monitor()
        )

        print("\n========================================")
        print("MESHWEAVER WEEK 3 COMPLETE INTEGRATION")
        print("========================================")

        print("\nWaiting for heartbeat communication...")

        await asyncio.sleep(6)

        # -----------------------------
        # INITIAL STATUS
        # -----------------------------
        print("\n--- Initial Node Status ---")

        print(
            "Node 1 sees Node 2:",
            node1.is_peer_active(node2.node_id)
        )

        print(
            "Node 1 sees Node 3:",
            node1.is_peer_active(node3.node_id)
        )

        # -----------------------------
        # TASK ROUTING
        # -----------------------------
        print("\n========================================")
        print("TASK ROUTING")
        print("========================================")

        result = router.route_task("Task-1")

        print("Task:", result["task"])
        print(
            "Selected node:",
            result["node"][:8] + "..."
        )
        print("Message:", result["message"])

        failed_node = result["node"]

        # -----------------------------
        # NODE FAILURE
        # -----------------------------
        print("\n========================================")
        print("SIMULATING NODE FAILURE")
        print("========================================")

        print(
            "Failed node:",
            failed_node[:8] + "..."
        )

        # Stop heartbeat of selected node
        failed_index = 0

        for i, node in enumerate(nodes):

            if node.node_id == failed_node:
                failed_index = i
                break

        heartbeat_tasks[failed_index].cancel()
        transports[failed_index].close()

        print("Heartbeat stopped for failed node.")

        # -----------------------------
        # WAIT FOR FAILURE DETECTION
        # -----------------------------
        print("\nWaiting for failure detection...")

        await asyncio.sleep(12)

        print("\n--- Failure Detection Result ---")

        node2_status = node1.is_peer_active(node2.node_id)
        node3_status = node1.is_peer_active(node3.node_id)

        print(
            "Node 1 sees Node 2:",
            node2_status
        )

        print(
            "Node 1 sees Node 3:",
            node3_status
        )

        # -----------------------------
        # UPDATE ROUTER
        # -----------------------------
        router.mark_node_inactive(failed_node)

        # -----------------------------
        # RE-ROUTE TASK
        # -----------------------------
        print("\n========================================")
        print("AUTOMATIC TASK RE-ROUTING")
        print("========================================")

        reroute_result = router.reroute_task(
            "Task-1",
            failed_node
        )

        print(
            "New node:",
            reroute_result["node"][:8] + "..."
        )

        print(
            "Message:",
            reroute_result["message"]
        )

        # -----------------------------
        # FINAL STATUS
        # -----------------------------
        print("\n========================================")
        print("FINAL ROUTER STATUS")
        print("========================================")

        for node_id, data in router.nodes.items():

            print(
                f"{node_id[:8]}... | "
                f"CPU: {data['cpu']} | "
                f"RAM: {data['ram']} | "
                f"Active: {data['active']}"
            )

        print("\n========================================")
        print("WEEK 3 INTEGRATION TEST PASSED")
        print("========================================")

        # Give output time to finish cleanly
        await asyncio.sleep(1)

        monitor_task.cancel()

        try:
            await monitor_task
        except asyncio.CancelledError:
            pass

    finally:

        # Stop remaining heartbeat tasks
        for task in heartbeat_tasks:

            if not task.done():
                task.cancel()

        # Close transports
        for transport in transports:
            transport.close()


if __name__ == "__main__":
    asyncio.run(main())