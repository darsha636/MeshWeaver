from node import KademliaNode


def main():
    # Create two independent Kademlia nodes
    node_a = KademliaNode(host="127.0.0.1", port=8000)
    node_b = KademliaNode(host="127.0.0.1", port=8001)

    print("===== Two-Node Kademlia Test =====")

    print("\nNode A")
    print(f"Node ID : {node_a.node_id}")
    print(f"Host    : {node_a.host}")
    print(f"Port    : {node_a.port}")

    print("\nNode B")
    print(f"Node ID : {node_b.node_id}")
    print(f"Host    : {node_b.host}")
    print(f"Port    : {node_b.port}")

    # Add Node B to Node A's routing table
    added = node_a.add_peer(
        node_b.node_id,
        node_b.host,
        node_b.port
    )

    print("\nAdding Node B to Node A routing table...")
    print(f"Added successfully: {added}")

    print(f"Node A peer count: {node_a.routing_table.count()}")

    # Verify Node B can be found
    found_peer = node_a.find_peer(node_b.node_id)

    print("\nSearching for Node B...")
    if found_peer:
        print("Node B found successfully.")
        print(f"Peer ID   : {found_peer.node_id}")
        print(f"Peer Host : {found_peer.host}")
        print(f"Peer Port : {found_peer.port}")
    else:
        print("Node B was not found.")

    # Display all peers known by Node A
    print("\nNode A routing table:")
    for peer in node_a.routing_table.get_peers():
        print(
            f"Node ID={peer.node_id}, "
            f"Host={peer.host}, "
            f"Port={peer.port}"
        )
    print("\nChecking node ID uniqueness...")

    if node_a.node_id != node_b.node_id:
        print("SUCCESS: Node IDs are unique.")
    else:
        print("ERROR: Node IDs are identical.")

if __name__ == "__main__":
    main()
    