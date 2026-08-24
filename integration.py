"""
MeshWeaver Week 2
Person 4 - Integration & Testing

Integrates:

1. Kademlia nodes
2. DHT peer discovery
3. Routing tables
4. CPU/RAM gossip
5. Multi-node testing
"""

import asyncio

from node import KademliaNode

from peer_discovery import (
    start_node,
    request_peers
)

from gossip import (
    GossipProtocol,
    create_gossip_message,
    GOSSIP_INTERVAL
)


class MeshWeaverNode:

    def __init__(
        self,
        node_number,
        discovery_port,
        gossip_port
    ):

        self.node_number = node_number

        self.node = KademliaNode(
            host="127.0.0.1",
            port=discovery_port,
            gossip_port=gossip_port
        )

        self.discovery_port = discovery_port
        self.gossip_port = gossip_port

        self.discovery_transport = None
        self.gossip_transport = None

    async def start(self):

        print(
            f"\nStarting Node {self.node_number}"
        )

        self.node.display_info()

        # Start DHT discovery.
        self.discovery_transport = (
            await start_node(self.node)
        )

        # Start gossip on a separate UDP port.
        loop = asyncio.get_running_loop()

        self.gossip_transport, _ = (
            await loop.create_datagram_endpoint(
                lambda: GossipProtocol(self.node),
                local_addr=(
                    self.node.host,
                    self.gossip_port
                )
            )
        )

        print(
            f"Gossip service running on "
            f"{self.node.host}:{self.gossip_port}"
        )

    async def stop(self):

        if self.discovery_transport:

            self.discovery_transport.close()

        if self.gossip_transport:

            self.gossip_transport.close()

    async def send_gossip(self):

        message = create_gossip_message(
            self.node
        )

        peers = (
            self.node.routing_table.get_peers()
        )

        if not peers:

            print(
                f"Node {self.node_number}: "
                f"No peers available for gossip."
            )

            return

        for peer in peers:

            address = (
                peer.host,
                peer.gossip_port
            )

            self.gossip_transport.sendto(
                message,
                address
            )

            print(
                f"Node {self.node_number} "
                f"sent gossip to "
                f"{peer.node_id[:8]} "
                f"at {address}"
            )


async def discover_nodes(nodes):

    print("\n" + "=" * 60)
    print("DHT PEER DISCOVERY")
    print("=" * 60)

    # Node 1 → Node 2
    await request_peers(
        nodes[0].discovery_transport,
        nodes[1].node.host,
        nodes[1].discovery_port
    )

    # Node 2 → Node 3
    await request_peers(
        nodes[1].discovery_transport,
        nodes[2].node.host,
        nodes[2].discovery_port
    )

    # Node 3 → Node 1
    await request_peers(
        nodes[2].discovery_transport,
        nodes[0].node.host,
        nodes[0].discovery_port
    )

    # Allow responses to arrive.
    await asyncio.sleep(2)


def display_routing_tables(nodes):

    print("\n" + "=" * 60)
    print("ROUTING TABLES")
    print("=" * 60)

    for mesh_node in nodes:

        node = mesh_node.node

        print(
            f"\nNode {mesh_node.node_number} "
            f"({node.node_id[:8]}...)"
        )

        peers = (
            node.routing_table.get_peers()
        )

        if not peers:

            print("  No peers discovered.")

        else:

            for peer in peers:

                print(
                    f"  Peer: "
                    f"{peer.node_id[:8]}..."
                )

                print(
                    f"    Discovery: "
                    f"{peer.host}:{peer.port}"
                )

                print(
                    f"    Gossip: "
                    f"{peer.host}:{peer.gossip_port}"
                )


async def gossip_test(nodes):

    print("\n" + "=" * 60)
    print("CPU/RAM GOSSIP TEST")
    print("=" * 60)

    for mesh_node in nodes:

        await mesh_node.send_gossip()

    # Give gossip messages time to arrive.
    await asyncio.sleep(2)


async def run_integration():

    print("\n" + "=" * 60)
    print("MESHWEAVER WEEK 2")
    print("PERSON 4 - INTEGRATION & TESTING")
    print("=" * 60)

    # Create three local nodes.
    nodes = [

        MeshWeaverNode(
            node_number=1,
            discovery_port=8000,
            gossip_port=9000
        ),

        MeshWeaverNode(
            node_number=2,
            discovery_port=8001,
            gossip_port=9001
        ),

        MeshWeaverNode(
            node_number=3,
            discovery_port=8002,
            gossip_port=9002
        )
    ]

    try:

        # -----------------------------------------
        # 1. Start nodes
        # -----------------------------------------

        print(
            "\n[1] Starting 3 MeshWeaver nodes..."
        )

        for node in nodes:

            await node.start()

        # -----------------------------------------
        # 2. Peer discovery
        # -----------------------------------------

        await discover_nodes(nodes)

        # -----------------------------------------
        # 3. Routing tables
        # -----------------------------------------

        display_routing_tables(nodes)

        # -----------------------------------------
        # 4. Gossip test
        # -----------------------------------------

        await gossip_test(nodes)

        # -----------------------------------------
        # 5. Continuous gossip
        # -----------------------------------------

        print("\n" + "=" * 60)

        print(
            f"Gossip will repeat approximately "
            f"every {GOSSIP_INTERVAL} seconds."
        )

        print(
            "Press CTRL+C to stop."
        )

        print("=" * 60)

        while True:

            await asyncio.sleep(
                GOSSIP_INTERVAL
            )

            for node in nodes:

                await node.send_gossip()

    except asyncio.CancelledError:

        pass

    finally:

        for node in nodes:

            await node.stop()

        print(
            "\nAll MeshWeaver nodes stopped."
        )


def main():

    try:

        asyncio.run(
            run_integration()
        )

    except KeyboardInterrupt:

        print(
            "\nIntegration stopped."
        )


if __name__ == "__main__":

    main()