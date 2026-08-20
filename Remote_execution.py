import asyncio
import cloudpickle


HOST = "127.0.0.1"
PORT = 9999


def add(a, b):
    return a + b


class RemoteExecutionProtocol(asyncio.DatagramProtocol):

    def __init__(self):
        self.transport = None
        self.result_received = asyncio.Event()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            # Deserialize the result received from the server
            result = cloudpickle.loads(data)

            print(f"Result: {result}")

            self.result_received.set()

        except Exception as e:
            print(f"Error receiving result: {e}")
            self.result_received.set()

    def error_received(self, exc):
        print(f"UDP error: {exc}")
        self.result_received.set()


async def send_function():

    loop = asyncio.get_running_loop()

    # Serialize function and arguments
    payload = cloudpickle.dumps((add, (10, 20)))

    # Create UDP connection
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: RemoteExecutionProtocol(),
        remote_addr=(HOST, PORT)
    )

    print("Sending serialized function to server...")

    # Send serialized function
    transport.sendto(payload)

    # Wait for server response
    try:
        await asyncio.wait_for(protocol.result_received.wait(), timeout=5)

    except asyncio.TimeoutError:
        print("Timeout: No response received from server.")

    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(send_function())