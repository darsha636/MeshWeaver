import asyncio
import cloudpickle
import json
import socket


HOST = "127.0.0.1"
PORT = 9999

DASHBOARD_HOST = "127.0.0.1"
DASHBOARD_PORT = 9100


def send_task_status(status, result=None):

    message = {
        "type": "task_status",
        "status": status,
        "result": result
    }

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    sock.sendto(
        json.dumps(message).encode(),
        (DASHBOARD_HOST, DASHBOARD_PORT)
    )

    sock.close()


class UDPServerProtocol(asyncio.DatagramProtocol):

    def connection_made(self, transport):

        self.transport = transport

        address = transport.get_extra_info("sockname")

        print(
            f"UDP Server started on "
            f"{address[0]}:{address[1]}"
        )

        print("Waiting for messages...")

    def datagram_received(self, data, addr):

        try:

            # Task received
            send_task_status("RUNNING")

            function, arguments = cloudpickle.loads(data)

            # Execute task
            result = function(*arguments)

            # Send result back to client
            response = cloudpickle.dumps(result)

            self.transport.sendto(
                response,
                addr
            )

            print(
                f"Executed function from {addr}"
            )

            print(
                f"Result: {result}"
            )

            # Task completed
            send_task_status(
                "COMPLETED",
                result
            )

        except Exception as e:

            print(
                f"Error: {e}"
            )

            send_task_status(
                "FAILED",
                str(e)
            )

    def error_received(self, exc):

        print(
            f"UDP error: {exc}"
        )

    def connection_lost(self, exc):

        print(
            "UDP server stopped."
        )


async def main():

    loop = asyncio.get_running_loop()

    transport, protocol = (
        await loop.create_datagram_endpoint(
            lambda: UDPServerProtocol(),
            local_addr=(HOST, PORT)
        )
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

        print(
            "\nServer stopped by user."
        )