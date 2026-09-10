import cloudpickle

from meshweaver.serialization import (
    serialize_task,
    deserialize_task,
    DeserializationError,
)


def test_cloudpickle_dependency():
    assert cloudpickle.__name__ == "cloudpickle"


def test_function_serialization():
    def add(a, b):
        return a + b

    data = serialize_task(add, args=(10, 20))

    assert isinstance(data, bytes)

    task = deserialize_task(data)

    assert task["function"](*task["args"], **task["kwargs"]) == 30


def test_positional_and_keyword_arguments():
    def calculate(a, b, multiplier=1):
        return (a + b) * multiplier

    data = serialize_task(
        calculate,
        args=(10, 20),
        kwargs={"multiplier": 5}
    )

    task = deserialize_task(data)

    assert task["args"] == (10, 20)
    assert task["kwargs"] == {"multiplier": 5}
    assert task["function"](*task["args"], **task["kwargs"]) == 150


def test_complex_function():
    factor = 10

    def complex_func(items, offset=2):
        return [x * factor + offset for x in items]

    data = serialize_task(
        complex_func,
        args=([1, 2, 3],),
        kwargs={"offset": 5}
    )

    task = deserialize_task(data)

    assert task["function"](*task["args"], **task["kwargs"]) == [
        15, 25, 35
    ]


def test_serialized_task_integrity():
    def dummy(x):
        return x * 2

    data = serialize_task(dummy, args=(5,))
    task = deserialize_task(data)

    assert "function" in task
    assert "args" in task
    assert "kwargs" in task
    assert callable(task["function"])


def test_invalid_function_raises_error():
    try:
        serialize_task("not_callable", args=(1,))
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError")


def test_corrupted_data_raises_error():
    try:
        deserialize_task(b"corrupted_binary_bytes_12345")
    except DeserializationError:
        pass
    else:
        raise AssertionError("Expected DeserializationError")