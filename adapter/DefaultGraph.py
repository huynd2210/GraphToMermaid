from adapter import MermaidAdapter

import networkx as nx

class DefaultGraph(MermaidAdapter.GraphToMermaidAdapter, MermaidAdapter.MermaidToGraphAdapter):
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, id, name=None, data=None):
        self.graph.add_node(id, name=name, data=data)

    def remove_node(self, node_id):
        self.graph.remove_node(node_id)

    def add_edge(self, id1, id2):
        self.graph.add_edge(id1, id2)

    def remove_edge(self, id1, id2):
        self.graph.remove_edge(id1, id2)

    def get_edges(self):
        return list(self.graph.edges())

    def get_node_label_by_id(self, identifier):
        return self.graph.nodes[identifier]["name"]

    def get_node_neighbors_id_by_id(self, identifier):
        return self.graph.neighbors(identifier)

    def getAllNodesId(self):
        return list(self.graph.nodes())

    def __str__(self):
        result = "Graph:\n"
        for node in self.graph.nodes():
            neighbors = list(self.graph.neighbors(node))
            result += f"{node} {self.graph.nodes[node]['name']} -> {neighbors}\n"
        return result
