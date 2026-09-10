# MeshWeaver — Zero-Dependency P2P Async Task Broker

MeshWeaver is a decentralized peer-to-peer task broker built with Python and `asyncio`.

Instead of relying on a central task broker such as RabbitMQ, MeshWeaver allows nodes to discover each other through a Kademlia-style Distributed Hash Table (DHT), exchange CPU/RAM information using a Gossip protocol, and route tasks to an available node based on system load.

The project also includes heartbeat-based failure detection, automatic task re-routing, TLS-secured communication, cryptographic task signatures, and a live terminal dashboard.

## Why MeshWeaver?

Traditional distributed task queues often depend on a central broker. This can create a single point of failure and introduce additional infrastructure requirements.

MeshWeaver follows a peer-to-peer approach where each node can participate in communication, resource sharing, task routing, and failure detection.

This architecture is particularly useful for distributed and edge-computing environments where lightweight communication between multiple machines is required     

## Architecture

        ┌─────────────┐        gossip (CPU/RAM)        ┌─────────────┐
        │   Node A    │ ◄─────────────────────────────► │   Node B    │
        │  (Kademlia) │                                  │  (Kademlia) │
        └──────┬──────┘                                  └──────┬──────┘
               │ peer discovery (DHT)                            │
               │ heartbeat monitoring                            │
               ▼                                                  ▼
        ┌─────────────┐        task routing (TLS)       ┌─────────────┐
        │   Node C    │ ◄─────────────────────────────► │   Node D    │
        └─────────────┘                                  └─────────────┘


## Key Features

* Asynchronous UDP communication using Python `asyncio`
* Kademlia-style peer discovery
* Distributed routing table
* CPU/RAM resource monitoring
* Gossip-based resource sharing
* Load-aware task routing
* Heartbeat-based node failure detection
* Automatic task re-routing after node failure
* Task serialization using `cloudpickle`
* TLS-encrypted task communication
* RSA digital signatures for task payload verification
* Live terminal dashboard using `rich`
* Automated testing with `pytest`

## Architecture

MeshWeaver is organized as a set of cooperating components:

Node
→ DHT / Peer Discovery
→ Routing Table
→ Gossip
→ CPU/RAM Load Information
→ Task Router
→ Heartbeat
→ Failure Detection
→ Task Re-routing
→ TLS + Digital Signatures
→ Live Dashboard

### Core Components

| Component       | Main Files                                                                                                              | Responsibility                                                     |
| --------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Node / DHT      | `node.py`, `peer_discovery.py`, `routing_table.py`                                                                      | Node identity, peer discovery, and routing information             |
| Gossip          | `gossip.py`, `load_reporter.py`, `node_load.py`                                                                         | Shares CPU/RAM information between peers                           |
| Task Routing    | `task_router.py`, `serialization.py`                                                                                    | Selects an active node based on reported load and serializes tasks |
| Fault Tolerance | `heartbeat.py`, `heartbeat_network.py`, `integration.py`                                                                | Detects unavailable peers and supports task re-routing             |
| Security        | `tls_security.py`, `signature_security.py`, `secure_task_client.py`, `secure_task_server.py`, `generate_certificate.py` | TLS transport and cryptographic task signatures                    |
| Dashboard       | `dashboard.py`, `dashboard_integration.py`                                                                              | Displays mesh topology, node load, and task state in the terminal  |

## Technology Stack

* Python 3.12+
* `asyncio`
* `cloudpickle`
* `psutil`
* `cryptography`
* `rich`
* `pytest`
* Git and GitHub

## Requirements

Python 3.12 or newer is recommended.

Install the project dependencies with:

```
python -m pip install -r requirements.txt
```

## Quick Start

### 1. Clone the repository

```
git clone https://github.com/darsha636/MeshWeaver.git
cd MeshWeaver
```

### 2. Install dependencies

```
python -m pip install -r requirements.txt
```

### 3. Generate the local TLS certificate

Run:

```
python -m src.meshweaver.generate_certificate
```

This creates:

* `certs/server.crt`
* `certs/server.key`

The certificate is self-signed and intended for local development and testing.

The private key is excluded from Git using `.gitignore`.

Never commit `certs/server.key`.

### 4. Run the multi-node integration demo

Run:

```
python -m src.meshweaver.integration
```

This starts multiple MeshWeaver nodes and demonstrates:

* Node creation
* Peer discovery
* Routing table population
* CPU/RAM gossip
* Heartbeat communication
* Failure detection

The integration demo can be stopped with `Ctrl+C`.

### 5. Run the live dashboard

Run:

```
python -m src.meshweaver.dashboard_integration
```

The dashboard displays:

* Mesh topology
* Node discovery/gossip information
* Node status
* CPU/RAM load
* Task execution state
* Task routing information

### 6. Run secure task execution

Start the secure server in one terminal:

```
python -m src.meshweaver.secure_task_server
```

Then start the client in another terminal:

```
python -m src.meshweaver.secure_task_client
```

The secure task demonstration uses:

* TLS encryption for communication
* RSA-PSS with SHA-256 for task signatures
* `cloudpickle` for task serialization

### 7. Run the test suite

Run:

```
python -m pytest tests -v
```

Current test result:

```
19 passed
```

The tests cover node creation, peer management, routing tables, serialization, task routing, load calculation, inactive-node handling, and task distribution.

## Development Timeline

MeshWeaver was developed over four weekly sprints by a five-person team. Each sprint added another layer to the distributed system.

### Week 1 — Networking Foundations

The first week established the basic communication layer.

Implemented:

* Asynchronous UDP server
* UDP client
* Basic message exchange
* Function serialization
* Remote execution foundation

The goal was to establish the communication and serialization mechanisms used by later components.

### Week 2 — DHT, Peer Discovery and Gossip

The second week extended the system into a multi-node network.

Implemented:

* Kademlia-style node identity
* Distributed routing table
* Peer discovery
* Gossip protocol
* CPU/RAM monitoring
* Multi-node integration

Nodes can discover peers and exchange resource information without depending on a central broker.

### Week 3 — Task Routing and Fault Tolerance

The third week introduced intelligent task routing and failure detection.

Implemented:

* Load-aware task routing
* CPU/RAM-based node selection
* UDP heartbeat monitoring
* Node failure detection
* Node recovery detection
* Automatic task re-routing

The system can exclude inactive nodes from task selection and route a task to another active node.

### Week 4 — Security and Live Dashboard

The fourth week focused on security and visualization.

Implemented:

* TLS-encrypted communication
* RSA digital signatures
* Secure task client/server
* Live Rich terminal dashboard
* Integrated heartbeat and task-routing visualization

The dashboard provides a real-time view of the mesh and task-routing state.

## Project Structure

```
MeshWeaver/
│
├── src/
│   └── meshweaver/
│       ├── __init__.py
│       ├── node.py
│       ├── routing_table.py
│       ├── peer_discovery.py
│       ├── gossip.py
│       ├── load_reporter.py
│       ├── node_load.py
│       ├── load_receiver.py
│       ├── task_router.py
│       ├── serialization.py
│       ├── heartbeat.py
│       ├── heartbeat_network.py
│       ├── integration.py
│       ├── tls_security.py
│       ├── signature_security.py
│       ├── secure_task_client.py
│       ├── secure_task_server.py
│       ├── generate_certificate.py
│       ├── dashboard.py
│       ├── dashboard_integration.py
│       ├── server.py
│       ├── client.py
│       └── Remote_execution.py
│
├── tests/
│   ├── test_nodes.py
│   ├── test_routing_table.py
│   ├── test_serialization.py
│   └── test_task_router.py
│
├── certs/
│   ├── server.crt
│   └── server.key
│
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

The `certs/server.key` file is generated locally and ignored by Git.

## Testing

MeshWeaver uses `pytest` for automated testing.

Run:

```
python -m pytest tests -v
```

Current result:

```
19 passed in 0.13s
```

The test suite currently validates:

* Node creation
* Unique node IDs
* Peer addition and lookup
* Routing table operations
* Duplicate peer handling
* Peer removal
* Task serialization
* Serialization error handling
* CPU/RAM load calculation
* Lowest-load node selection
* Task routing
* Inactive node exclusion
* Multiple task distribution

## Security

MeshWeaver uses two security mechanisms.

### TLS

TLS encrypts communication between the secure task client and server so that task data is not transmitted as plaintext over the network.

### Digital Signatures

Task payloads are signed using RSA-PSS with SHA-256.

The receiving side verifies the signature before executing the task.

The current implementation demonstrates payload integrity and signature verification using the supplied public key.

For a production deployment, the system should use a trusted public-key registry, certificate authority, or another mechanism for establishing and validating peer identities.

## Fault Tolerance

MeshWeaver uses heartbeat messages to monitor peer availability.

Nodes periodically send heartbeat messages to their known peers.

If a peer stops responding for longer than the configured timeout, it can be marked inactive.

The task router then avoids inactive nodes and can re-route tasks to another available node.

Example flow:

```
Task
  ↓
Node B selected
  ↓
Node B fails
  ↓
Heartbeat timeout
  ↓
Node B marked inactive
  ↓
Task re-routed
  ↓
Node C selected
```

## Current Limitations

This project is a learning and prototype implementation of a decentralized task broker.

Current areas for improvement include:

* Stronger trusted-peer identity management
* More comprehensive end-to-end task execution across multiple physical machines
* Improved heartbeat state synchronization
* Retry and exponential backoff for failed task delivery
* Larger multi-node stress testing
* Production-grade certificate management
* Persistent task state and recovery

## Future Improvements

Possible future enhancements include:

* Trusted public-key registry
* Automatic node bootstrapping
* Better Kademlia routing
* Task retry and backoff
* Persistent task queues
* Distributed task result storage
* Docker-based multi-node deployment
* Kubernetes/edge deployment experiments
* Performance benchmarking with 10+ nodes
* Test coverage reporting

## Team

MeshWeaver was developed by a five-person team across four weekly sprints.

Each sprint focused on a different layer of the system:

* Networking
* DHT and peer discovery
* Gossip and resource monitoring
* Task routing
* Fault tolerance
* Security
* Live visualization

The project demonstrates how independent distributed-system components can be integrated into a lightweight peer-to-peer task broker.

## License

This project is intended for educational and research purposes.
