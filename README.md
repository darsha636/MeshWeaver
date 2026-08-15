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

## Files

### server.py

Contains the asynchronous UDP server.

### client.py

A simple UDP client used to test the server.

### README.md

Contains project documentation and instructions.

## Requirements

- Python 3
- No external packages are required.

## How to Run

### 1. Start the UDP Server

Open a terminal and run:

```bash
python server.py
