import asyncio
import ssl


class TLSServerProtocol(asyncio.Protocol):

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        peer = transport.get_extra_info("peername")

        print(f"[TLS] Secure connection established with {peer}")

    def data_received(self, data):
        message = data.decode("utf-8")

        print(f"[TLS] Encrypted message received: {message}")

        response = "Secure TLS message received"
        self.transport.write(response.encode("utf-8"))

    def connection_lost(self, exc):
        print("[TLS] Secure connection closed")


async def start_tls_server(
    host="127.0.0.1",
    port=8443,
    certfile="certs/server.crt",
    keyfile="certs/server.key"
):

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    ssl_context.load_cert_chain(
        certfile=certfile,
        keyfile=keyfile
    )

    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        TLSServerProtocol,
        host,
        port,
        ssl=ssl_context
    )

    print(f"[TLS] Server running on {host}:{port}")

    return server


async def tls_client(
    host="127.0.0.1",
    port=8443,
    cafile="certs/server.crt",
    message="Hello from MeshWeaver"
):

    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
        cafile=cafile
    )

    reader, writer = await asyncio.open_connection(
        host,
        port,
        ssl=ssl_context,
        server_hostname="localhost"
    )

    print("[TLS] Secure connection established")

    writer.write(message.encode("utf-8"))
    await writer.drain()

    response = await reader.read(1024)

    print("[TLS] Server response:", response.decode("utf-8"))

    writer.close()
    await writer.wait_closed()

    print("[TLS] Secure connection closed")


async def main():
    server = await start_tls_server()

    await asyncio.sleep(1)

    await tls_client()

    server.close()
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())