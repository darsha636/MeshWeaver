import asyncio
import json
import time

import psutil


GOSSIP_INTERVAL = 5


class GossipProtocol(asyncio.DatagramProtocol):

    def __init__(self, node):
        self.node = node
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

        address = transport.get_extra_info("sockname")

        print(
            f"Gossip started on "
            f"{address[0]}:{address[1]}"
        )

    def datagram_received(self, data, addr):
        try:
            message = json.loads(data.decode("utf-8"))

            if message.get("type") != "gossip":
                return

            node_id = message.get("node_id")
            cpu = message.get("cpu_percent")
            ram = message.get("ram_percent")

            print("\nReceived gossip:")
            print(f"From node : {node_id}")
            print(f"CPU       : {cpu}%")
            print(f"RAM       : {ram}%")
            print(f"Address   : {addr}")

        except Exception as e:
            print(f"Error processing gossip: {e}")


def create_gossip_message(node):
    cpu_usage = psutil.cpu_percent(interval=0.1)
    ram_usage = psutil.virtual_memory().percent

    message = {
        "type": "gossip",
        "node_id": node.node_id,
        "cpu_percent": cpu_usage,
        "ram_percent": ram_usage,
        "timestamp": time.time()
    }

    return json.dumps(message).encode("utf-8")


async def gossip_loop(node, transport):

    while True:

        message = create_gossip_message(node)

        peers = node.routing_table.get_peers()

        if not peers:
            print("\nNo known peers to gossip with.")

        for peer in peers:

            address = (peer.host, peer.port)

            transport.sendto(message, address)

            print(
                f"\nGossip sent to "
                f"{peer.node_id} at {address}"
            )

        await asyncio.sleep(GOSSIP_INTERVAL)


async def start_gossip(node):

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: GossipProtocol(node),
        local_addr=(node.host, node.port)
    )

    try:
        await gossip_loop(node, transport)

    except asyncio.CancelledError:
        pass

    finally:
        transport.close()


if __name__ == "__main__":

    from node import KademliaNode

    node = KademliaNode(
        host="127.0.0.1",
        port=8000
    )

    node.display_info()

    asyncio.run(start_gossip(node))