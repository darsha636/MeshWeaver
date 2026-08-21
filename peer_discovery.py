import asyncio
import json
import sys

from node import KademliaNode


DISCOVER_PEERS = "DISCOVER_PEERS"
PEER_LIST = "PEER_LIST"


class PeerDiscoveryProtocol(asyncio.DatagramProtocol):

    def __init__(self, node):
        self.node = node
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

        print(
            f"Discovery service started on "
            f"{self.node.host}:{self.node.port}"
        )

    def datagram_received(self, data, addr):
        try:
            message = json.loads(
                data.decode("utf-8")
            )

            if message.get("type") == DISCOVER_PEERS:
                self.send_peer_list(addr)

            elif message.get("type") == PEER_LIST:
                self.add_discovered_peers(message)

        except Exception as e:
            print(
                f"Error processing message: {e}"
            )

    def send_peer_list(self, addr):

        peers = []

        # This node
        peers.append({
            "node_id": self.node.node_id,
            "host": self.node.host,
            "port": self.node.port,
            "gossip_port": self.node.gossip_port
        })

        # Known peers
        for peer in self.node.routing_table.get_peers():

            peers.append({
                "node_id": peer.node_id,
                "host": peer.host,
                "port": peer.port,
                "gossip_port": peer.gossip_port
            })

        response = {
            "type": PEER_LIST,
            "peers": peers
        }

        self.transport.sendto(
            json.dumps(response).encode("utf-8"),
            addr
        )

        print(
            f"Sent {len(peers)} known peer(s) to {addr}"
        )

    def add_discovered_peers(self, message):

        peers = message.get("peers", [])

        for peer in peers:

            if peer["node_id"] == self.node.node_id:
                continue

            added = self.node.add_peer(
                peer["node_id"],
                peer["host"],
                peer["port"],
                peer.get("gossip_port")
            )

            if added:

                print(
                    f"Discovered peer: "
                    f"{peer['node_id']} "
                    f"{peer['host']}:{peer['port']} "
                    f"(gossip: "
                    f"{peer.get('gossip_port')})"
                )


async def start_node(node):

    loop = asyncio.get_running_loop()

    transport, protocol = (
        await loop.create_datagram_endpoint(
            lambda: PeerDiscoveryProtocol(node),
            local_addr=(
                node.host,
                node.port
            )
        )
    )

    return transport


async def request_peers(
    node,
    peer_host,
    peer_port
):

    # Send discovery request using a temporary UDP socket.
    loop = asyncio.get_running_loop()

    transport, _ = (
        await loop.create_datagram_endpoint(
            lambda: asyncio.DatagramProtocol(),
            local_addr=(node.host, 0)
        )
    )

    message = {
        "type": DISCOVER_PEERS
    }

    transport.sendto(
        json.dumps(message).encode("utf-8"),
        (peer_host, peer_port)
    )

    print(
        f"Discovery request sent to "
        f"{peer_host}:{peer_port}"
    )

    transport.close()


async def main():

    if len(sys.argv) < 2:

        print(
            "Usage: py peer_discovery.py <port>"
        )

        print(
            "Example: py peer_discovery.py 8000"
        )

        return

    port = int(sys.argv[1])

    node = KademliaNode(
        host="127.0.0.1",
        port=port
    )

    print(
        "\n===== DHT Peer Discovery Node ====="
    )

    node.display_info()

    transport = await start_node(node)

    try:

        if port == 8000:

            await asyncio.sleep(2)

            await request_peers(
                node,
                "127.0.0.1",
                8001
            )

        else:

            print(
                f"Node {port} is waiting "
                f"for discovery requests..."
            )

        await asyncio.Future()

    except asyncio.CancelledError:
        pass

    finally:

        transport.close()


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nNode stopped.")