from dataclasses import dataclass


@dataclass
class Peer:
    """Stores information about another MeshWeaver node."""
    
    node_id: str
    host: str
    port: int


class RoutingTable:
    """Basic routing table for storing known peers."""

    def __init__(self):
        self.peers = []

    def add_peer(self, peer):
        """Add a peer if it is not already present."""
        for existing_peer in self.peers:
            if existing_peer.node_id == peer.node_id:
                return False

        self.peers.append(peer)
        return True

    def remove_peer(self, node_id):
        """Remove a peer using its node ID."""
        for peer in self.peers:
            if peer.node_id == node_id:
                self.peers.remove(peer)
                return True

        return False

    def get_peers(self):
        """Return all known peers."""
        return self.peers

    def count(self):
        """Return the number of known peers."""
        return len(self.peers)