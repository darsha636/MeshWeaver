from meshweaver.task_router import TaskRouter


router = TaskRouter()

# Add three nodes with different loads
router.update_node_load("NODE1", 80, 70)
router.update_node_load("NODE2", 30, 40)
router.update_node_load("NODE3", 50, 50)

print("========================================")
print("WEEK 3 TASK ROUTING & RE-ROUTING TEST")
print("========================================")

# Initial routing
result = router.route_task("Task-1")

print("\n--- Initial Routing ---")
print("Selected node:", result["node"])
print("Message:", result["message"])

# Simulate selected node failure
failed_node = result["node"]

print("\n--- Node Failure ---")
print("Failed node:", failed_node)

router.mark_node_inactive(failed_node)

# Re-route task
result = router.reroute_task(
    "Task-1",
    failed_node
)

print("\n--- Re-Routing ---")
print("New node:", result["node"])
print("Message:", result["message"])

# Final status
print("\n--- Final Status ---")
for node_id, data in router.nodes.items():
    print(
        node_id,
        "CPU:", data["cpu"],
        "RAM:", data["ram"],
        "Active:", data["active"]
    )
