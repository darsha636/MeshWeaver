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
        """Add a peer if the node ID is not already present."""
        if self.find_peer(peer.node_id) is not None:
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

    def find_peer(self, node_id):
        """Find a peer using its node ID."""
        for peer in self.peers:
            if peer.node_id == node_id:
                return peer

        return None

    def get_peers(self):
        """Return all known peers."""
        return list(self.peers)

    def count(self):
        """Return the number of known peers."""
        return len(self.peers)

    def clear(self):
        """Remove all peers from the routing table."""
        self.peers.clear()