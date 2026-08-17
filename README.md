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
- Dependencies listed in `requirements.txt` (`cloudpickle`)

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
```

---

## Function Serialization (Person 3)

### Overview

The function serialization module (`serialization.py`) provides capability to convert Python functions and their arguments into binary payloads suitable for network transmission in MeshWeaver.

### Key Concepts

1. **Why `cloudpickle`?**: Standard Python `pickle` cannot serialize lambda functions, nested functions, or dynamically generated functions. `cloudpickle` extends Python's default pickle module to serialize almost any Python callable object across process and network boundaries.
2. **What Gets Serialized**:
   - The target callable Python function.
   - Positional arguments (`args`).
   - Keyword arguments (`kwargs`).
3. **Packaging**: Functions and arguments are packaged into a structured dictionary:
   ```python
   {
       "function": function,
       "args": args,
       "kwargs": kwargs
   }
   ```
   and converted into a binary payload using `cloudpickle.dumps()`.
4. **Deserialization & Execution**: The receiver restores the dictionary using `cloudpickle.loads()`, validates the callable, and executes the function with unpacked arguments (`function(*args, **kwargs)`).

### Usage Example

```python
from serialization import serialize_task, deserialize_task

def my_function(a, b):
    return a + b

# Serialize task
task_data = serialize_task(my_function, (10, 20), {})

# Deserialize task
task = deserialize_task(task_data)
function = task["function"]
args = task["args"]
kwargs = task["kwargs"]

# Execute restored function
result = function(*args, **kwargs)
print(result)  # Output: 30
```

### Running Serialization Tests

Run the serialization test suite directly using Python:

```bash
python test_serialization.py
```