import asyncio
import json


class LoadReceiver(asyncio.DatagramProtocol):

    def datagram_received(self, data, addr):
        try:
            load_info = json.loads(data.decode())

            print("\n===== Load Report Received =====")
            print(f"Node ID : {load_info['node_id']}")
            print(f"Host    : {load_info['host']}")
            print(f"Port    : {load_info['port']}")
            print(f"CPU     : {load_info['cpu']}%")
            print(f"RAM     : {load_info['ram']}%")
            print("================================")

        except (json.JSONDecodeError, KeyError) as error:
            print(f"Invalid load report: {error}")


async def main():
    loop = asyncio.get_running_loop()

    transport, _ = await loop.create_datagram_endpoint(
        LoadReceiver,
        local_addr=("127.0.0.1", 9000)
    )

    print("Load receiver started on 127.0.0.1:9000")

    try:
        await asyncio.Future()
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())