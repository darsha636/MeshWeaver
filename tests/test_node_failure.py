import asyncio

from meshweaver.node import KademliaNode
from meshweaver.heartbeat_network import start_heartbeat, send_heartbeats


async def main():

    # Create 3 nodes
    node1 = KademliaNode(
        host="127.0.0.1",
        port=8100,
        gossip_port=9100
    )

    node2 = KademliaNode(
        host="127.0.0.1",
        port=8101,
        gossip_port=9101
    )

    node3 = KademliaNode(
        host="127.0.0.1",
        port=8102,
        gossip_port=9102
    )

    nodes = [node1, node2, node3]

    transports = []
    heartbeat_tasks = []
    monitor_tasks = []

    try:

        # Add peers
        node1.add_peer(
            node2.node_id,
            node2.host,
            node2.port,
            node2.gossip_port
        )

        node1.add_peer(
            node3.node_id,
            node3.host,
            node3.port,
            node3.gossip_port
        )

        node2.add_peer(
            node1.node_id,
            node1.host,
            node1.port,
            node1.gossip_port
        )

        node3.add_peer(
            node1.node_id,
            node1.host,
            node1.port,
            node1.gossip_port
        )

        # Start heartbeat services
        for node in nodes:

            transport = await start_heartbeat(node)

            transports.append(transport)

            heartbeat_tasks.append(
                asyncio.create_task(
                    send_heartbeats(node, transport)
                )
            )

            monitor_tasks.append(
                asyncio.create_task(
                    node.start_heartbeat_monitor()
                )
            )

        print("\n========================================")
        print("3 NODE HEARTBEAT FAILURE TEST")
        print("========================================")

        print("\nAll nodes are running.")
        print("Waiting for heartbeats...")

        await asyncio.sleep(6)

        print("\n--- Initial Status ---")

        print(
            "Node 1 sees Node 2:",
            node1.is_peer_active(node2.node_id)
        )

        print(
            "Node 1 sees Node 3:",
            node1.is_peer_active(node3.node_id)
        )

        # Simulate Node 2 failure
        print("\n========================================")
        print("SIMULATING NODE 2 FAILURE")
        print("========================================")

        heartbeat_tasks[1].cancel()

        transports[1].close()

        print("Node 2 heartbeat stopped.")

        print("\nWaiting for heartbeat timeout...")
        await asyncio.sleep(12)

        print("\n--- After Failure ---")

        print(
            "Node 1 sees Node 2:",
            node1.is_peer_active(node2.node_id)
        )

        print(
            "Node 1 sees Node 3:",
            node1.is_peer_active(node3.node_id)
        )

    finally:

        for task in heartbeat_tasks:
            task.cancel()

        for task in monitor_tasks:
            task.cancel()

        for transport in transports:
            transport.close()

        print("\nTest completed.")


if __name__ == "__main__":
    asyncio.run(main())
