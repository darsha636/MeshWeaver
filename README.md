# MeshWeaver - UDP Networking

## Week 1 - UDP Server

This project is part of MeshWeaver, a zero-dependency P2P async task broker.

### Objective

The objective of Week 1 is to create a UDP server using Python's `asyncio` module.

The server:

- Listens for incoming UDP messages.
- Receives messages from clients.
- Decodes the received message.
- Sends a response back to the client.

### Files

- `server.py` - UDP server implementation.
- `client.py` - UDP client implementation.
- `README.md` - Project documentation.

### Requirements

- Python 3.x
- No external dependencies required.

---

## Person 2 - UDP Client

The UDP client is implemented using Python's `asyncio` module.

### Responsibilities

- Sends messages to the UDP server.
- Receives responses from the UDP server.
- Decodes and displays the server response.
- Communicates with the UDP server asynchronously.

### Testing

The UDP client was tested successfully with the UDP server running on localhost.

### Communication Flow

UDP Client → Sends Message → UDP Server → Sends Response → UDP Client

### Running the UDP Client

Start the UDP server first:

```bash
python server.py