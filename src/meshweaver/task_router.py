class TaskRouter:
    def __init__(self):
        self.nodes = {}

    def update_node_load(self, node_id, cpu, ram):
        self.nodes[node_id] = {
            "cpu": cpu,
            "ram": ram,
            "active": True
        }

    def mark_node_inactive(self, node_id):
        if node_id in self.nodes:
            self.nodes[node_id]["active"] = False

    def mark_node_active(self, node_id):
        if node_id in self.nodes:
            self.nodes[node_id]["active"] = True

    def calculate_load(self, cpu, ram):
        return (cpu + ram) / 2

    def select_node(self, exclude=None):
        active_nodes = {
            node_id: data
            for node_id, data in self.nodes.items()
            if data["active"] and node_id != exclude
        }

        if not active_nodes:
            return None

        return min(
            active_nodes,
            key=lambda node_id: self.calculate_load(
                active_nodes[node_id]["cpu"],
                active_nodes[node_id]["ram"]
            )
        )

    def route_task(self, task):
        selected_node = self.select_node()

        if selected_node is None:
            return {
                "success": False,
                "message": "No active node available",
                "node": None,
                "task": task
            }

        return {
            "success": True,
            "message": "Task routed successfully",
            "node": selected_node,
            "task": task
        }

    def reroute_task(self, task, failed_node):
        """
        Re-route a task when the assigned node fails.
        """

        self.mark_node_inactive(failed_node)

        new_node = self.select_node(exclude=failed_node)

        if new_node is None:
            return {
                "success": False,
                "message": "No active node available for re-routing",
                "node": None,
                "task": task
            }

        return {
            "success": True,
            "message": "Task re-routed successfully",
            "node": new_node,
            "task": task
        }
