import psutil
import asyncio
import sys

from node import KademliaNode
from load_reporter import send_load_report


async def monitor_load(node):
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent

        load_info = {
            "node_id": node.node_id,
            "host": node.host,
            "port": node.port,
            "cpu": cpu,
            "ram": ram
        }

        send_load_report(load_info)

        print(
            f"Node: {load_info['node_id'][:8]}... | "
            f"Port: {load_info['port']} | "
            f"CPU: {load_info['cpu']}% | "
            f"RAM: {load_info['ram']}%"
        )

        await asyncio.sleep(5)


async def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001

    node = KademliaNode(
        host="127.0.0.1",
        port=port
    )

    await monitor_load(node)


if __name__ == "__main__":
    asyncio.run(main())