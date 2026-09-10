from meshweaver.node import KademliaNode


node = KademliaNode(
    host="127.0.0.1",
    port=8000,
    gossip_port=9000
)

# Add another node as a peer
node.add_peer(
    node_id="NODE2",
    host="127.0.0.1",
    port=8001,
    gossip_port=9001
)

print("NODE2 active:", node.is_peer_active("NODE2"))

# Simulate heartbeat
node.receive_heartbeat("NODE2")

print("Heartbeat received from NODE2")
print("NODE2 active:", node.is_peer_active("NODE2"))

print("Active peers:", node.get_active_peers())
