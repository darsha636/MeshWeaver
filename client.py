import asyncio

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999


class UDPClientProtocol(asyncio.DatagramProtocol):

    def connection_made(self, transport):
        self.transport = transport

        message = input("Enter message: ")

        print(f"Sending message: {message}")

        self.transport.sendto(
            message.encode("utf-8"),
            (SERVER_HOST, SERVER_PORT)
        )

    def datagram_received(self, data, addr):
        response = data.decode("utf-8")

        print(f"Server response: {response}")

        self.transport.close()

    def error_received(self, exc):
        print(f"UDP error: {exc}")

    def connection_lost(self, exc):
        print("UDP client stopped.")


async def main():

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPClientProtocol(),
        remote_addr=(SERVER_HOST, SERVER_PORT)
    )

    try:
        await asyncio.sleep(5)

    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())