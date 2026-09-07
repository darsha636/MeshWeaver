import asyncio
import ssl
import cloudpickle

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


HOST = "127.0.0.1"
PORT = 8444


class SecureTaskServer:

    async def handle_client(self, reader, writer):

        address = writer.get_extra_info("peername")

        print(f"[TLS] Secure client connected: {address}")

        try:

            data = await reader.read(65536)

            if not data:
                return

            task_data = cloudpickle.loads(data)

            function = task_data["function"]
            arguments = task_data["arguments"]
            signature = task_data["signature"]

            # Rebuild public key
            public_key = serialization.load_pem_public_key(
                task_data["public_key"]
            )

            # Recreate exactly the same data that was signed
            signed_data = cloudpickle.dumps(
                (function, arguments)
            )

            # Verify signature
            try:

                public_key.verify(
                    signature,
                    signed_data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )

                print("[SECURITY] Signature verification: PASSED")
                print("[SECURITY] Task request is authentic.")

            except Exception:

                print("[SECURITY] Signature verification: FAILED")

                response = {
                    "success": False,
                    "message": "Invalid signature"
                }

                writer.write(cloudpickle.dumps(response))
                await writer.drain()

                return

            # Execute verified task
            result = function(*arguments)

            print("[TASK] Task executed successfully")
            print(f"[TASK] Result: {result}")

            response = {
                "success": True,
                "result": result
            }

            writer.write(
                cloudpickle.dumps(response)
            )

            await writer.drain()

        except Exception as e:

            print(f"[ERROR] {e}")

        finally:

            writer.close()
            await writer.wait_closed()

            print("[TLS] Secure client connection closed")


async def main():

    ssl_context = ssl.SSLContext(
        ssl.PROTOCOL_TLS_SERVER
    )

    ssl_context.load_cert_chain(
        certfile="certs/server.crt",
        keyfile="certs/server.key"
    )

    server = await asyncio.start_server(
        SecureTaskServer().handle_client,
        HOST,
        PORT,
        ssl=ssl_context
    )

    print("========================================")
    print("MESHWEAVER SECURE TASK SERVER")
    print("========================================")
    print(f"[TLS] Server running on {HOST}:{PORT}")
    print("[SECURITY] TLS + Digital Signature enabled")
    print("Waiting for secure task...")
    print("========================================")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nSecure server stopped.")