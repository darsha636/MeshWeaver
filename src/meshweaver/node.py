import hashlib
import os
import asyncio

from .routing_table import RoutingTable, Peer
from .heartbeat import HeartbeatMonitor


class KademliaNode:
    def __init__(
        self,
        host="127.0.0.1",
        port=8000,
        gossip_port=None
    ):
        self.host = host
        self.port = port

        # Gossip uses a separate UDP port.
        self.gossip_port = (
            gossip_port
            if gossip_port is not None
            else port + 1000
        )

        # Generate a unique 160-bit Kademlia node ID.
        random_data = os.urandom(32)
        self.node_id = hashlib.sha1(
            random_data
        ).hexdigest()

        # Initialize routing table.
        self.routing_table = RoutingTable()

        # Initialize heartbeat monitor.
        self.heartbeat_monitor = HeartbeatMonitor(
            self.node_id,
            timeout=10
        )

    def add_peer(
        self,
        node_id,
        host,
        port,
        gossip_port=None
    ):
        """Add another node to the routing table."""

        if self.routing_table.find_peer(node_id):
            return False

        if gossip_port is None:
            gossip_port = port + 1000

        new_peer = Peer(
            node_id=node_id,
            host=host,
            port=port,
            gossip_port=gossip_port
        )

        result = self.routing_table.add_peer(new_peer)

        # Add peer to heartbeat monitoring.
        if result:
            self.heartbeat_monitor.add_peer(node_id)

        return result

    def remove_peer(self, node_id):
        """Remove a node from the routing table."""
        return self.routing_table.remove_peer(node_id)

    def find_peer(self, node_id):
        """Find a node in the routing table."""
        return self.routing_table.find_peer(node_id)

    def receive_heartbeat(self, node_id):
        """Record a heartbeat received from a peer."""
        self.heartbeat_monitor.receive_heartbeat(node_id)

    def is_peer_active(self, node_id):
        """Check whether a peer is active."""
        return self.heartbeat_monitor.is_active(node_id)

    def get_active_peers(self):
        """Return all active peers."""
        return self.heartbeat_monitor.get_active_peers()

    async def start_heartbeat_monitor(self):
        """Start monitoring peer heartbeats."""
        await self.heartbeat_monitor.check_heartbeats()

    def display_info(self):
        print("===== MeshWeaver Kademlia Node =====")
        print(f"Node ID     : {self.node_id}")
        print(f"Host        : {self.host}")
        print(f"Discovery   : {self.port}")
        print(f"Gossip      : {self.gossip_port}")
        print(f"Peers       : {self.routing_table.count()}")
        print("Heartbeat monitor initialized.")
        print("Routing table initialized successfully.")
        print("Node initialized successfully.")


if __name__ == "__main__":
    node = KademliaNode()
    node.display_info()
