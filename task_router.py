class TaskRouter:
    def __init__(self):
        self.nodes = {}

    def update_node_load(self, node_id, cpu, ram):
        """
        Update CPU and RAM information for a node.
        """
        self.nodes[node_id] = {
            "cpu": cpu,
            "ram": ram,
            "active": True
        }

    def mark_node_inactive(self, node_id):
        """
        Mark a node as inactive.
        """
        if node_id in self.nodes:
            self.nodes[node_id]["active"] = False

    def calculate_load(self, cpu, ram):
        """
        Calculate the overall load of a node.
        CPU and RAM are given equal importance.
        """
        return (cpu + ram) / 2

    def select_node(self):
        """
        Select the active node with the lowest load.
        """
        active_nodes = {
            node_id: data
            for node_id, data in self.nodes.items()
            if data["active"]
        }

        if not active_nodes:
            return None

        selected_node = min(
            active_nodes,
            key=lambda node_id: self.calculate_load(
                active_nodes[node_id]["cpu"],
                active_nodes[node_id]["ram"]
            )
        )

        return selected_node

    def route_task(self, task):
        """
        Select the best node and assign the task to it.
        """
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