from adapter import MermaidAdapter
from mermaid_builder.mermaid_builder import NodeShape
import networkx as nx
# import matplotlib.pyplot as plt

class DefaultGraph(MermaidAdapter.GraphToMermaidAdapter, MermaidAdapter.MermaidToGraphAdapter):
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, id, name=None, data=None, shape=NodeShape.RECT_ROUND):
        self.graph.add_node(id, name=name, data=data, shape=shape)

    def remove_node(self, node_id):
        self.graph.remove_node(node_id)

    def add_edge(self, id1, id2, description = ""):
        self.graph.add_edge(id1, id2, description=description)

    def remove_edge(self, id1, id2):
        self.graph.remove_edge(id1, id2)

    def get_edges(self):
        return list(self.graph.edges())

    def get_node_label_by_id(self, identifier):
        return self.graph.nodes[identifier]["name"]

    def get_node_shape_by_id(self, identifier):
        return self.graph.nodes[identifier]["shape"]

    def get_node_neighbors_id_by_id(self, identifier):
        return self.graph.neighbors(identifier)

    def getAllNodesId(self):
        return list(self.graph.nodes())

    def get_all_edges_description(self):
        return nx.get_edge_attributes(self.graph, "description")

    def get_edges_description(self, id1, id2):
        return self.get_all_edges_description()[(id1, id2)] 
    
    '''
    def show_graph(self):
        pos = nx.planar_layout(self.graph)
        labels = self.get_all_edges_description()
        nx.draw_networkx_nodes(self.graph, pos = pos, node_size=700)
        nx.draw_networkx_edges(
            self.graph, pos, width=3, alpha=0.5, style="dashed", arrows=True, arrowstyle="->"
        )
        nx.draw_networkx_labels(self.graph, pos = pos, font_size = 10, font_family = "sans-serif")
        nx.draw_networkx_edge_labels(self.graph, pos = pos,
                                     edge_labels=labels, font_color="blue",
                                     font_family="sans-serif", clip_on = False)
        plt.draw()
        plt.show()
    '''

    def __str__(self):
        result = "Graph:\n"
        for node in self.graph.nodes():
            neighbors = list(self.graph.neighbors(node))
            result += f"{node} {self.get_node_label_by_id(node)} -> {str(neighbors)[1:-1]}\n"
        # self.show_graph()
        return result
