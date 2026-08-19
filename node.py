import hashlib
import os


class KademliaNode:
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port

        # Generate a unique 160-bit Kademlia node ID
        random_data = os.urandom(32)
        self.node_id = hashlib.sha1(random_data).hexdigest()

        # Basic routing table / peer list
        self.routing_table = []

    def display_info(self):
        print("===== MeshWeaver Kademlia Node =====")
        print(f"Node ID : {self.node_id}")
        print(f"Host    : {self.host}")
        print(f"Port    : {self.port}")
        print(f"Peers   : {len(self.routing_table)}")
        print("Node initialized successfully.")


if __name__ == "__main__":
    node = KademliaNode()
    node.display_info()