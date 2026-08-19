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

        # Initialize the basic routing table
        self.routing_table = RoutingTable()

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