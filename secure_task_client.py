import asyncio
import ssl
import cloudpickle

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


HOST = "127.0.0.1"
PORT = 8444


def add(a, b):
    return a + b


async def main():

    # Generate RSA keys
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    # Task
    function = add
    arguments = (10, 20)

    # Create data that will be signed
    signed_data = cloudpickle.dumps(
        (function, arguments)
    )

    # Create digital signature
    signature = private_key.sign(
        signed_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Convert public key to bytes
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Package task
    task_data = {
        "function": function,
        "arguments": arguments,
        "signature": signature,
        "public_key": public_key_bytes
    }

    # TLS configuration
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
        cafile="certs/server.crt"
    )

    # Connect to TLS server
    reader, writer = await asyncio.open_connection(
        HOST,
        PORT,
        ssl=ssl_context,
        server_hostname="localhost"
    )

    print("========================================")
    print("MESHWEAVER SECURE TASK CLIENT")
    print("========================================")
    print("[SECURITY] Task signature generated")
    print("[TLS] Secure connection established")
    print("[TASK] Sending signed task...")

    # Send task
    writer.write(cloudpickle.dumps(task_data))
    await writer.drain()

    # Receive response
    response_data = await reader.read(65536)

    if response_data:
        response = cloudpickle.loads(response_data)
        print("[SERVER] Response received:", response)
    else:
        print("[SERVER] No response received")

    writer.close()
    await writer.wait_closed()

    print("[TLS] Secure connection closed")
    print("========================================")


if __name__ == "__main__":
    asyncio.run(main())