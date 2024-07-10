from src.main import MermaidAdapter
from src.main.default_data_structures.DefaultNode import DefaultNode


class DefaultGraph(MermaidAdapter.GraphToMermaidAdapter, MermaidAdapter.MermaidToGraphAdapter):
    def __init__(self):
        self.nodes = {}

    def add_node(self, id, name=None, data=None):
        if id not in self.nodes:
            self.nodes[id] = DefaultNode(id, name, data)
        return self.nodes[id]

    def remove_node(self, node_id):
        if node_id in self.nodes:
            node = self.nodes[node_id]
            for neighbor in list(node.neighbors):
                node.remove_neighbor(neighbor)
            del self.nodes[node_id]

    def add_edge(self, id1, id2):
        if id1 in self.nodes and id2 in self.nodes:
            node1 = self.nodes[id1]
            node2 = self.nodes[id2]
            node1.add_neighbor(node2)

    def remove_edge(self, id1, id2):
        if id1 in self.nodes and id2 in self.nodes:
            node1 = self.nodes[id1]
            node2 = self.nodes[id2]
            node1.remove_neighbor(node2)

    def get_nodes(self):
        return list(self.nodes.values())

    def get_edges(self):
        edges = set()
        for node in self.nodes.values():
            for neighbor in node.neighbors:
                edge = tuple(sorted([node.id, neighbor.id]))
                edges.add(edge)
        return list(edges)

    def get_node_by_name(self, name):
        for node in self.nodes.values():
            if node.name == name:
                return node
        return None

    def get_node_label_by_id(self, identifier):
        return self.nodes[identifier].name

    def get_node_neighbors_id_by_id(self, identifier):
        return [neighbor.id for neighbor in self.nodes[identifier].neighbors]
    def getAllNodesId(self):
        return list(self.nodes.keys())

    def __str__(self):
        result = "Graph:\n"
        for node in self.nodes.values():
            neighbors = ", ".join(str(neighbor.id) for neighbor in node.neighbors)
            result += f"Node {node.id} ('{node.name}'): {neighbors}\n"
        return result