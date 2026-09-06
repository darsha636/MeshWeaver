import asyncio
import json

from rich.console import Console, Group
from rich.live import Live
from rich.table import Table


console = Console()

nodes = {}
peer_counts = {}
routing_info = {}

task_status = "IDLE"
task_result = ""


class DashboardReceiver(asyncio.DatagramProtocol):

    def datagram_received(self, data, addr):

        global task_status
        global task_result

        try:
            info = json.loads(data.decode())

            message_type = info.get("type")

            # CPU / RAM
            if message_type is None:

                node_id = info["node_id"]

                nodes[node_id] = {
                    "host": info["host"],
                    "port": info["port"],
                    "cpu": info["cpu"],
                    "ram": info["ram"],
                    "status": "ONLINE"
                }

            # Peer information
            elif message_type == "peer_status":

                node_id = info["node_id"]

                peer_counts[node_id] = info["peer_count"]

            # Routing information
            elif message_type == "routing_status":

                node_id = info["node_id"]

                routing_info[node_id] = info["peers"]

            # Task information
            elif message_type == "task_status":

                task_status = info["status"]

                if info.get("result") is not None:
                    task_result = str(info["result"])

        except (json.JSONDecodeError, KeyError) as error:

            console.print(
                f"Invalid dashboard message: {error}"
            )


def create_node_table():

    table = Table(
        title="MeshWeaver Node Dashboard"
    )

    table.add_column("Node ID")
    table.add_column("Host")
    table.add_column("Port")
    table.add_column("CPU")
    table.add_column("RAM")
    table.add_column("Peers")
    table.add_column("Status")

    for node_id, info in nodes.items():

        table.add_row(
            node_id[:8] + "...",
            info["host"],
            str(info["port"]),
            f'{info["cpu"]:.1f}%',
            f'{info["ram"]:.1f}%',
            str(peer_counts.get(node_id, 0)),
            info["status"]
        )

    return table


def create_task_table():

    table = Table(
        title="Task Status"
    )

    table.add_column("Status")
    table.add_column("Result")

    table.add_row(
        task_status,
        task_result if task_result else "-"
    )

    return table


def create_routing_table():

    table = Table(
        title="Routing Information"
    )

    table.add_column("Node ID")
    table.add_column("Peer ID")
    table.add_column("Discovery")
    table.add_column("Gossip")

    for node_id, peers in routing_info.items():

        if not peers:

            table.add_row(
                node_id[:8] + "...",
                "No peers",
                "-",
                "-"
            )

        else:

            for peer in peers:

                table.add_row(
                    node_id[:8] + "...",
                    peer["node_id"][:8] + "...",
                    f'{peer["host"]}:{peer["port"]}',
                    f'{peer["host"]}:{peer["gossip_port"]}'
                )

    return table


def create_dashboard():

    return Group(
        create_node_table(),
        create_task_table(),
        create_routing_table()
    )


async def main():

    loop = asyncio.get_running_loop()

    transport, _ = await loop.create_datagram_endpoint(
        DashboardReceiver,
        local_addr=("127.0.0.1", 9100)
    )

    console.print(
        "[bold]MeshWeaver Dashboard started "
        "on 127.0.0.1:9100[/bold]"
    )

    try:

        with Live(
            create_dashboard(),
            refresh_per_second=1,
            console=console,
            screen=True
        ) as live:

            while True:

                live.update(
                    create_dashboard(),
                    refresh=True
                )

                await asyncio.sleep(1)

    except KeyboardInterrupt:

        pass

    finally:

        transport.close()

        console.print(
            "\nDashboard stopped."
        )


if __name__ == "__main__":

    asyncio.run(main())