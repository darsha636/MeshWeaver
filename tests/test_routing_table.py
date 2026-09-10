from meshweaver.routing_table import Peer, RoutingTable


def test_add_peer():
    routing_table = RoutingTable()

    peer = Peer(
        node_id="node-001",
        host="127.0.0.1",
        port=8001,
        gossip_port=9001
    )

    assert routing_table.add_peer(peer) is True
    assert routing_table.count() == 1


def test_find_peer():
    routing_table = RoutingTable()

    peer = Peer(
        node_id="node-001",
        host="127.0.0.1",
        port=8001,
        gossip_port=9001
    )

    routing_table.add_peer(peer)

    found = routing_table.find_peer("node-001")

    assert found is not None
    assert found.node_id == "node-001"
    assert found.host == "127.0.0.1"
    assert found.port == 8001
    assert found.gossip_port == 9001


def test_duplicate_peer_is_rejected():
    routing_table = RoutingTable()

    peer = Peer(
        node_id="node-001",
        host="127.0.0.1",
        port=8001,
        gossip_port=9001
    )

    assert routing_table.add_peer(peer) is True
    assert routing_table.add_peer(peer) is False
    assert routing_table.count() == 1


def test_remove_peer():
    routing_table = RoutingTable()

    peer = Peer(
        node_id="node-001",
        host="127.0.0.1",
        port=8001,
        gossip_port=9001
    )

    routing_table.add_peer(peer)

    assert routing_table.remove_peer("node-001") is True
    assert routing_table.count() == 0
    assert routing_table.find_peer("node-001") is None
