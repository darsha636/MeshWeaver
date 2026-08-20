"""
Complete end-to-end verification suite for Person 3 Function Serialization.
"""

import sys
import serialization
from serialization import (
    serialize_task,
    deserialize_task,
    SerializationError,
    DeserializationError,
)


def check_dependency():
    import cloudpickle
    assert cloudpickle.__name__ == "cloudpickle"
    print("[PASS] cloudpickle import")


def check_basic_serialization():
    def add(a, b):
        return a + b

    data = serialize_task(add, args=(10, 20))
    assert isinstance(data, bytes)
    task = deserialize_task(data)
    res = task["function"](*task["args"], **task["kwargs"])
    assert res == 30, f"Expected 30, got {res}"


def check_arguments():
    def calculate(a, b, multiplier=1):
        return (a + b) * multiplier

    data = serialize_task(calculate, args=(10, 20), kwargs={"multiplier": 5})
    task = deserialize_task(data)
    assert task["args"] == (10, 20)
    assert task["kwargs"] == {"multiplier": 5}
    res = task["function"](*task["args"], **task["kwargs"])
    assert res == 150, f"Expected 150, got {res}"


def check_complex_function():
    factor = 10
    def complex_func(items, offset=2):
        return [x * factor + offset for x in items]

    data = serialize_task(complex_func, args=([1, 2, 3],), kwargs={"offset": 5})
    task = deserialize_task(data)
    res = task["function"](*task["args"], **task["kwargs"])
    assert res == [15, 25, 35], f"Expected [15, 25, 35], got {res}"


def check_integrity():
    def dummy(x):
        return x * 2

    data = serialize_task(dummy, args=(5,))
    assert isinstance(data, bytes), "serialize_task must return bytes"
    task = deserialize_task(data)
    assert "function" in task and "args" in task and "kwargs" in task
    assert callable(task["function"])


def check_error_handling():
    # Test invalid function input
    try:
        serialize_task("not_callable", args=(1,))
        raise AssertionError("Should have raised TypeError for non-callable function")
    except TypeError:
        pass

    # Test corrupted serialized data
    try:
        deserialize_task(b"corrupted_binary_bytes_12345")
        raise AssertionError("Should have raised DeserializationError for corrupted payload")
    except DeserializationError:
        pass


def run_all_checks():
    check_dependency()

    check_basic_serialization()
    print("[PASS] Function serialization")

    check_arguments()
    print("[PASS] Positional arguments")
    print("[PASS] Keyword arguments")

    check_complex_function()
    check_integrity()
    print("[PASS] Function deserialization")
    print("[PASS] Restored function execution")
    print("[PASS] Result verification")

    check_error_handling()
    print("[PASS] Error handling")


if __name__ == "__main__":
    run_all_checks()
