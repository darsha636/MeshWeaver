import asyncio
import cloudpickle


HOST = "127.0.0.1"
PORT = 9999


def add(a, b):
    return a + b


async def send_function():
    loop = asyncio.get_running_loop()

    # Serialize function and arguments
    payload = cloudpickle.dumps((add, (10, 20)))

    # Create UDP connection
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: asyncio.DatagramProtocol(),
        remote_addr=(HOST, PORT)
    )

    print("Sending serialized function to server...")

    # Send serialized function
    transport.sendto(payload)

    # Keep connection open briefly
    await asyncio.sleep(1)

    transport.close()


if __name__ == "__main__":
    asyncio.run(send_function())