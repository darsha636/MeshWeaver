import asyncio
import cloudpickle

HOST = "127.0.0.1"
PORT = 9999


class UDPServerProtocol(asyncio.DatagramProtocol):

    def connection_made(self, transport):
        self.transport = transport
        address = transport.get_extra_info("sockname")

        print(f"UDP Server started on {address[0]}:{address[1]}")
        print("Waiting for messages...")

    def datagram_received(self, data, addr):
        try:
            function, arguments = cloudpickle.loads(data)

            result = function(*arguments)

            response = cloudpickle.dumps(result)

            self.transport.sendto(response, addr)

            print(f"Executed function from {addr}")
            print(f"Result: {result}")

        except Exception as e:
            print(f"Error: {e}")

    def error_received(self, exc):
        print(f"UDP error: {exc}")

    def connection_lost(self, exc):
        print("UDP server stopped.")


async def main():

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(),
        local_addr=(HOST, PORT)
    )

    try:
        await asyncio.Future()

    except asyncio.CancelledError:
        pass

    finally:
        transport.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nServer stopped by user.")