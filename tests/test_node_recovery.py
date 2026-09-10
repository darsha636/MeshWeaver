import asyncio

from meshweaver.node import KademliaNode
from meshweaver.heartbeat_network import start_heartbeat, send_heartbeats


async def main():

    # Create Node 1 and Node 2
    node1 = KademliaNode(
        host="127.0.0.1",
        port=8200,
        gossip_port=9200
    )

    node2 = KademliaNode(
        host="127.0.0.1",
        port=8201,
        gossip_port=9201
    )

    # Add each other as peers
    node1.add_peer(
        node2.node_id,
        node2.host,
        node2.port,
        node2.gossip_port
    )

    node2.add_peer(
        node1.node_id,
        node1.host,
        node1.port,
        node1.gossip_port
    )

    transports = []
    heartbeat_tasks = []
    monitor_tasks = []

    try:

        # Start heartbeat services
        for node in [node1, node2]:

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
        print("NODE FAILURE AND RECOVERY TEST")
        print("========================================")

        print("\nBoth nodes are running.")
        print("Waiting for heartbeats...")

        await asyncio.sleep(6)

        print("\n--- Initial Status ---")

        print(
            "Node 1 sees Node 2:",
            node1.is_peer_active(node2.node_id)
        )

        # -----------------------------------------
        # Simulate Node 2 failure
        # -----------------------------------------

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

        # -----------------------------------------
        # Recover Node 2
        # -----------------------------------------

        print("\n========================================")
        print("RECOVERING NODE 2")
        print("========================================")

        # Start Node 2 heartbeat service again
        transports[1] = await start_heartbeat(node2)

        heartbeat_tasks[1] = asyncio.create_task(
            send_heartbeats(
                node2,
                transports[1]
            )
        )

        print("Node 2 heartbeat restarted.")

        print("\nWaiting for recovery heartbeat...")

        await asyncio.sleep(5)

        print("\n--- After Recovery ---")

        print(
            "Node 1 sees Node 2:",
            node1.is_peer_active(node2.node_id)
        )

    finally:

        for task in heartbeat_tasks:
            if task:
                task.cancel()

        for task in monitor_tasks:
            if task:
                task.cancel()

        for transport in transports:
            if transport:
                transport.close()

        print("\nTest completed.")


if __name__ == "__main__":
    asyncio.run(main())
