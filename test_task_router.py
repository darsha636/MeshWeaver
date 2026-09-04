from task_router import TaskRouter


def test_select_lowest_load_node():
    router = TaskRouter()

    router.update_node_load("node1", 80, 70)
    router.update_node_load("node2", 30, 40)
    router.update_node_load("node3", 50, 60)

    assert router.select_node() == "node2"


def test_cpu_ram_load_calculation():
    router = TaskRouter()

    load = router.calculate_load(40, 60)

    assert load == 50


def test_route_task():
    router = TaskRouter()

    router.update_node_load("node1", 70, 80)
    router.update_node_load("node2", 20, 30)

    result = router.route_task("Hello Mesh")

    assert result["success"] is True
    assert result["node"] == "node2"
    assert result["task"] == "Hello Mesh"


def test_no_active_node():
    router = TaskRouter()

    result = router.route_task("Test Task")

    assert result["success"] is False
    assert result["node"] is None


def test_inactive_node_is_not_selected():
    router = TaskRouter()

    router.update_node_load("node1", 10, 20)
    router.update_node_load("node2", 50, 60)

    router.mark_node_inactive("node1")

    assert router.select_node() == "node2"


def test_multiple_task_distribution():
    router = TaskRouter()

    router.update_node_load("node1", 20, 30)
    router.update_node_load("node2", 60, 70)
    router.update_node_load("node3", 40, 50)

    result1 = router.route_task("Task 1")
    result2 = router.route_task("Task 2")

    assert result1["node"] == "node1"
    assert result2["node"] == "node1"