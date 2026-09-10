from meshweaver.node import KademliaNode


def test_node_creation():
    node_a = KademliaNode(host="127.0.0.1", port=8000)
    node_b = KademliaNode(host="127.0.0.1", port=8001)

    assert node_a.node_id != node_b.node_id
    assert node_a.host == "127.0.0.1"
    assert node_b.host == "127.0.0.1"
    assert node_a.port == 8000
    assert node_b.port == 8001


def test_add_and_find_peer():
    node_a = KademliaNode(host="127.0.0.1", port=8000)
    node_b = KademliaNode(host="127.0.0.1", port=8001)

    added = node_a.add_peer(
        node_b.node_id,
        node_b.host,
        node_b.port
    )

    assert added is True
    assert node_a.routing_table.count() == 1

    found_peer = node_a.find_peer(node_b.node_id)

    assert found_peer is not None
    assert found_peer.node_id == node_b.node_id