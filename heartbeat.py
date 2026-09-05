import asyncio
import time


class HeartbeatMonitor:
    def __init__(self, node_id, timeout=10):
        self.node_id = node_id
        self.timeout = timeout
        self.peers = {}

    def add_peer(self, peer_id):
        self.peers[peer_id] = {
            "last_seen": time.time(),
            "active": True
        }

    def receive_heartbeat(self, peer_id):
        if peer_id not in self.peers:
            self.add_peer(peer_id)

        self.peers[peer_id]["last_seen"] = time.time()

        if not self.peers[peer_id]["active"]:
            print(f"[RECOVERY] Node {peer_id} is active again")

        self.peers[peer_id]["active"] = True

    async def check_heartbeats(self):
        while True:
            current_time = time.time()

            for peer_id, info in self.peers.items():
                if current_time - info["last_seen"] > self.timeout:
                    if info["active"]:
                        info["active"] = False
                        print(f"[FAILURE] Node {peer_id} is inactive")

            await asyncio.sleep(2)

    def is_active(self, peer_id):
        return (
            peer_id in self.peers
            and self.peers[peer_id]["active"]
        )

    def get_active_peers(self):
        return [
            peer_id
            for peer_id, info in self.peers.items()
            if info["active"]
        ]