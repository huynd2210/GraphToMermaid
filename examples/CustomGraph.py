
"""
Example of a custom graph class.
Simple inherits from the GraphToMermaidAdapter for conversion from graph to mermaid
and MermaidToGraphAdapter for conversion from mermaid to graph.
"""
from examples.CustomNode import CustomNode
from adapter import MermaidAdapter


class CustomGraph(MermaidAdapter.GraphToMermaidAdapter, MermaidAdapter.MermaidToGraphAdapter):
    def __init__(self):
        self.nodeCollection = {}
        self.next_id = 1

    def add_node(self, name, data=None):
        node_id = self.next_id
        self.next_id += 1
        if node_id not in self.nodeCollection:
            self.nodeCollection[node_id] = CustomNode(node_id, name, data)
        return self.nodeCollection[node_id]

    def remove_node(self, node_id):
        if node_id in self.nodeCollection:
            node = self.nodeCollection[node_id]
            for neighbor in list(node.neighbors):
                node.remove_neighbor(neighbor)
            del self.nodeCollection[node_id]

    def add_edge(self, id1, id2):
        if id1 in self.nodeCollection and id2 in self.nodeCollection:
            node1 = self.nodeCollection[id1]
            node2 = self.nodeCollection[id2]
            node1.add_neighbor(node2)

    def remove_edge(self, id1, id2):
        if id1 in self.nodeCollection and id2 in self.nodeCollection:
            node1 = self.nodeCollection[id1]
            node2 = self.nodeCollection[id2]
            node1.remove_neighbor(node2)

    def get_nodes(self):
        return list(self.nodeCollection.values())

    def get_edges(self):
        edges = set()
        for node in self.nodeCollection.values():
            for neighbor in node.neighbors:
                edge = tuple(sorted([node.id, neighbor.id]))
                edges.add(edge)
        return list(edges)

    def get_node_by_name(self, name):
        for node in self.nodeCollection.values():
            if node.name == name:
                return node
        return None

    def get_node_label_by_id(self, identifier):
        return self.nodeCollection[identifier].name

    def get_node_neighbors_id_by_id(self, identifier):
        return [neighbor.id for neighbor in self.nodeCollection[identifier].neighbors]
    def getAllNodesId(self):
        return list(self.nodeCollection.keys())

    def __str__(self):
        result = "Graph:\n"
        for node in self.nodeCollection.values():
            neighbors = ", ".join(str(neighbor.id) for neighbor in node.neighbors)
            result += f"Node {node.id} ('{node.name}'): {neighbors}\n"
        return result