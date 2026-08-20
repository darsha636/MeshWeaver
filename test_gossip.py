import asyncio

from node import KademliaNode
from gossip import start_gossip


async def main():

    # Create two nodes
    node_a = KademliaNode(
        host="127.0.0.1",
        port=8000
    )

    node_b = KademliaNode(
        host="127.0.0.1",
        port=8001
    )

    # Add Node B to Node A
    node_a.add_peer(
        node_b.node_id,
        node_b.host,
        node_b.port
    )

    # Add Node A to Node B
    node_b.add_peer(
        node_a.node_id,
        node_a.host,
        node_a.port
    )

    print("\n===== Gossip Test =====")

    print(
        f"Node A: {node_a.node_id} "
        f"{node_a.host}:{node_a.port}"
    )

    print(
        f"Node B: {node_b.node_id} "
        f"{node_b.host}:{node_b.port}"
    )

    print(f"Node A peers: {node_a.routing_table.count()}")
    print(f"Node B peers: {node_b.routing_table.count()}")

    # Start gossip for both nodes
    await asyncio.gather(
        start_gossip(node_a),
        start_gossip(node_b)
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nGossip test stopped.")