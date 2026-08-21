import hashlib
import os

from routing_table import RoutingTable, Peer


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

    def add_peer(
        self,
        node_id,
        host,
        port,
        gossip_port=None
    ):
        """Add another node to the routing table."""

        peer = self.routing_table.find_peer(node_id)

        if peer is not None:
            return False

        if gossip_port is None:
            gossip_port = port + 1000

        new_peer = Peer(
            node_id=node_id,
            host=host,
            port=port,
            gossip_port=gossip_port
        )

        return self.routing_table.add_peer(new_peer)

    def remove_peer(self, node_id):
        """Remove a node from the routing table."""
        return self.routing_table.remove_peer(node_id)

    def find_peer(self, node_id):
        """Find a node in the routing table."""
        return self.routing_table.find_peer(node_id)

    def display_info(self):
        print("===== MeshWeaver Kademlia Node =====")
        print(f"Node ID     : {self.node_id}")
        print(f"Host        : {self.host}")
        print(f"Discovery   : {self.port}")
        print(f"Gossip      : {self.gossip_port}")
        print(f"Peers       : {self.routing_table.count()}")
        print("Routing table initialized successfully.")
        print("Node initialized successfully.")


if __name__ == "__main__":
    node = KademliaNode()
    node.display_info()