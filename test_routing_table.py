from routing_table import Peer, RoutingTable


def main():
    print("===== MeshWeaver Routing Table Test =====")

    routing_table = RoutingTable()

    # Create sample peers
    peer1 = Peer(
        node_id="node-001",
        host="127.0.0.1",
        port=8001
    )

    peer2 = Peer(
        node_id="node-002",
        host="127.0.0.1",
        port=8002
    )

    # Test adding peers
    print("\nAdding peers...")

    print("Peer 1:", routing_table.add_peer(peer1))
    print("Peer 2:", routing_table.add_peer(peer2))

    print("Total peers:", routing_table.count())

    # Test finding a peer
    print("\nFinding node-001...")

    found = routing_table.find_peer("node-001")

    if found:
        print("Peer found successfully.")
        print(f"Node ID : {found.node_id}")
        print(f"Host    : {found.host}")
        print(f"Port    : {found.port}")
    else:
        print("Peer not found.")

    # Test duplicate protection
    print("\nTesting duplicate peer...")

    duplicate = routing_table.add_peer(peer1)

    print("Duplicate added:", duplicate)

    # Test removing a peer
    print("\nRemoving node-001...")

    removed = routing_table.remove_peer("node-001")

    print("Removed successfully:", removed)
    print("Remaining peers:", routing_table.count())

    # Final validation
    print("\n===== Validation Result =====")

    if routing_table.count() == 1:
        print("SUCCESS: Routing table operations are working correctly.")
    else:
        print("ERROR: Routing table validation failed.")


if __name__ == "__main__":
    main()