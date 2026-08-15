import asyncio

HOST = "127.0.0.1"
PORT = 9999


class UDPServerProtocol(asyncio.DatagramProtocol):

    def connection_made(self, transport):
        self.transport = transport
        address = transport.get_extra_info("sockname")

        print(f"UDP Server started on {address[0]}:{address[1]}")
        print("Waiting for messages...")

    def datagram_received(self, data, addr):
        message = data.decode("utf-8")

        print(f"Received from {addr}: {message}")

        response = f"Server received: {message}"

        self.transport.sendto(
            response.encode("utf-8"),
            addr
        )

        print(f"Response sent to {addr}")

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