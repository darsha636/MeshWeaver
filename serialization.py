"""
Function Serialization Module for MeshWeaver (Person 3).

Provides reusable functions to serialize and deserialize Python functions along
with their positional and keyword arguments using cloudpickle.
"""

from typing import Any, Callable, Dict, Optional, Tuple, Union
import cloudpickle


class SerializationError(Exception):
    """Raised when task serialization fails."""
    pass


class DeserializationError(Exception):
    """Raised when task deserialization fails or payload is corrupted."""
    pass


def serialize_task(
    function: Callable[..., Any],
    args: Optional[Union[Tuple[Any, ...], list]] = None,
    kwargs: Optional[Dict[str, Any]] = None
) -> bytes:
    """
    Serializes a callable Python function along with positional and keyword arguments.

    Args:
        function: The target callable function to serialize.
        args: Positional arguments for the function. Defaults to empty tuple.
        kwargs: Keyword arguments for the function. Defaults to empty dict.

    Returns:
        bytes: The cloudpickle-serialized task binary payload.

    Raises:
        TypeError: If function is not callable or args/kwargs have invalid types.
        SerializationError: If cloudpickle fails to serialize the task object.
    """
    if not callable(function):
        raise TypeError(f"Invalid function input: expected a callable object, got {type(function).__name__}")

    if args is None:
        args = ()
    elif not isinstance(args, (tuple, list)):
        raise TypeError(f"Positional arguments 'args' must be a tuple or list, got {type(args).__name__}")
    else:
        args = tuple(args)

    if kwargs is None:
        kwargs = {}
    elif not isinstance(kwargs, dict):
        raise TypeError(f"Keyword arguments 'kwargs' must be a dict, got {type(kwargs).__name__}")

    task = {
        "function": function,
        "args": args,
        "kwargs": kwargs
    }

    try:
        return cloudpickle.dumps(task)
    except Exception as exc:
        raise SerializationError(f"Failed to serialize task payload: {exc}") from exc


def deserialize_task(data: bytes) -> Dict[str, Any]:
    """
    Deserializes binary data back into a task dictionary containing the
    restored function, positional arguments, and keyword arguments.

    Args:
        data: The serialized bytes payload.

    Returns:
        Dict[str, Any]: Dictionary containing 'function', 'args', and 'kwargs'.

    Raises:
        TypeError: If data is not of type bytes or bytearray.
        DeserializationError: If deserialization fails or data is corrupted/invalid.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"Expected bytes or bytearray payload, got {type(data).__name__}")

    try:
        task = cloudpickle.loads(data)
    except Exception as exc:
        raise DeserializationError(f"Corrupted or invalid serialized data: {exc}") from exc

    if not isinstance(task, dict):
        raise DeserializationError(f"Invalid payload format: expected dict, got {type(task).__name__}")

    for required_key in ("function", "args", "kwargs"):
        if required_key not in task:
            raise DeserializationError(f"Invalid task structure: missing key '{required_key}'")

    if not callable(task["function"]):
        raise DeserializationError("Deserialized 'function' is not callable")

    return task
