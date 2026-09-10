import asyncio
import json

from .heartbeat import HeartbeatMonitor


HEARTBEAT = "HEARTBEAT"
HEARTBEAT_INTERVAL = 3


class HeartbeatProtocol(asyncio.DatagramProtocol):

    def __init__(self, node):
        self.node = node
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

        print(
            f"Heartbeat service started on "
            f"{self.node.host}:{self.node.port + 2000}"
        )

    def datagram_received(self, data, addr):
        try:
            message = json.loads(data.decode("utf-8"))

            if message.get("type") == HEARTBEAT:
                node_id = message.get("node_id")

                self.node.receive_heartbeat(node_id)

                print(
                    f"[HEARTBEAT] Received from "
                    f"{node_id[:8]}..."
                )

        except Exception as e:
            print(f"Heartbeat error: {e}")


async def start_heartbeat(node):

    loop = asyncio.get_running_loop()

    heartbeat_port = node.port + 2000

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: HeartbeatProtocol(node),
        local_addr=(node.host, heartbeat_port)
    )

    return transport


async def send_heartbeats(node, transport):

    while True:

        peers = node.routing_table.get_peers()

        for peer in peers:

            message = {
                "type": HEARTBEAT,
                "node_id": node.node_id
            }

            transport.sendto(
                json.dumps(message).encode("utf-8"),
                (
                    peer.host,
                    peer.port + 2000
                )
            )

            print(
                f"[HEARTBEAT] Node "
                f"{node.node_id[:8]}... "
                f"sent to {peer.node_id[:8]}..."
            )

        await asyncio.sleep(HEARTBEAT_INTERVAL)
