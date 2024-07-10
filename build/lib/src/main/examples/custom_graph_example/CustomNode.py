
"""
Example of a custom node class for a graph
"""
class CustomNode:
    def __init__(self, id, name, data=None):
        self.id = id
        self.name = name
        self.data = data
        self.neighbors = set()

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)
        neighbor.neighbors.add(self)

    def remove_neighbor(self, neighbor):
        self.neighbors.discard(neighbor)
        neighbor.neighbors.discard(self)

    def __repr__(self):
        return f"Node(id={self.id}, name='{self.name}', data={self.data})"

