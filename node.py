import hashlib
import os

from routing_table import RoutingTable


class KademliaNode:
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port

        # Generate a unique 160-bit Kademlia node ID
        random_data = os.urandom(32)
        self.node_id = hashlib.sha1(random_data).hexdigest()

        # Initialize routing table
        self.routing_table = RoutingTable()

    def add_peer(self, node_id, host, port):
        """Add another node to the routing table."""
        peer = self.routing_table.find_peer(node_id)

        if peer is not None:
            return False

        from routing_table import Peer

        new_peer = Peer(
            node_id=node_id,
            host=host,
            port=port
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
        print(f"Node ID : {self.node_id}")
        print(f"Host    : {self.host}")
        print(f"Port    : {self.port}")
        print(f"Peers   : {self.routing_table.count()}")
        print("Routing table initialized successfully.")
        print("Node initialized successfully.")


if __name__ == "__main__":
    node = KademliaNode()
    node.display_info()