"""
MeshWeaver Week 3
Person 3 - Fault Tolerance

Integrates:

1. Kademlia nodes
2. DHT peer discovery
3. Routing tables
4. CPU/RAM gossip
5. Multi-node testing
6. UDP heartbeat monitoring
7. Node failure detection
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

from heartbeat_network import (
    start_heartbeat,
    send_heartbeats
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

        # Heartbeat components
        self.heartbeat_transport = None
        self.heartbeat_task = None
        self.heartbeat_monitor_task = None

    async def start(self):

        print(
            f"\nStarting Node {self.node_number}"
        )

        self.node.display_info()

        # -----------------------------------------
        # 1. Start DHT discovery
        # -----------------------------------------

        self.discovery_transport = (
            await start_node(self.node)
        )

        # -----------------------------------------
        # 2. Start Gossip service
        # -----------------------------------------

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

        # -----------------------------------------
        # 3. Start Heartbeat service
        # -----------------------------------------

        self.heartbeat_transport = (
            await start_heartbeat(self.node)
        )

        # Send heartbeat periodically
        self.heartbeat_task = asyncio.create_task(
            send_heartbeats(
                self.node,
                self.heartbeat_transport
            )
        )

        # Monitor heartbeat timeout
        self.heartbeat_monitor_task = asyncio.create_task(
            self.node.start_heartbeat_monitor()
        )

        print(
            f"Heartbeat service running on "
            f"{self.node.host}:{self.node.port + 2000}"
        )

    async def stop(self):

        # -----------------------------------------
        # Stop heartbeat
        # -----------------------------------------

        if self.heartbeat_task:
            self.heartbeat_task.cancel()

        if self.heartbeat_monitor_task:
            self.heartbeat_monitor_task.cancel()

        if self.heartbeat_transport:
            self.heartbeat_transport.close()

        # -----------------------------------------
        # Stop discovery
        # -----------------------------------------

        if self.discovery_transport:
            self.discovery_transport.close()

        # -----------------------------------------
        # Stop gossip
        # -----------------------------------------

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

    # Allow responses to arrive
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

                print(
                    f"    Heartbeat: "
                    f"{peer.host}:{peer.port + 2000}"
                )


async def gossip_test(nodes):

    print("\n" + "=" * 60)
    print("CPU/RAM GOSSIP TEST")
    print("=" * 60)

    for mesh_node in nodes:

        await mesh_node.send_gossip()

    # Give gossip messages time to arrive
    await asyncio.sleep(2)


def display_heartbeat_status(nodes):

    print("\n" + "=" * 60)
    print("HEARTBEAT STATUS")
    print("=" * 60)

    for mesh_node in nodes:

        active_peers = (
            mesh_node.node.get_active_peers()
        )

        print(
            f"Node {mesh_node.node_number}: "
            f"{len(active_peers)} active peer(s)"
        )

        for peer_id in active_peers:

            print(
                f"  ACTIVE: {peer_id[:8]}..."
            )


async def run_integration():

    print("\n" + "=" * 60)
    print("MESHWEAVER WEEK 3")
    print("PERSON 3 - FAULT TOLERANCE")
    print("=" * 60)

    # -----------------------------------------
    # Create three local nodes
    # -----------------------------------------

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
        # 5. Heartbeat status
        # -----------------------------------------

        display_heartbeat_status(nodes)

        # -----------------------------------------
        # 6. Continuous operation
        # -----------------------------------------

        print("\n" + "=" * 60)

        print(
            f"Gossip will repeat approximately "
            f"every {GOSSIP_INTERVAL} seconds."
        )

        print(
            "Heartbeat is sent approximately "
            "every 3 seconds."
        )

        print(
            "Heartbeat timeout is 10 seconds."
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