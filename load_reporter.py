import json
import socket


def send_load_report(load_info, host="127.0.0.1", port=9000):
    message = json.dumps(load_info).encode()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(message, (host, port))

    print(
        f"Load report sent -> {host}:{port}"
    )

    sock.close()