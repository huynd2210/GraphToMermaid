from abc import ABC, abstractmethod
from typing import List

import networkx as nx

"""
This is an interface that defines the interface for converting a graph to a Mermaid string.`
"""
class GraphToMermaidAdapter(ABC, nx.Graph):

    @abstractmethod
    def get_node_label_by_id(self, identifier) -> str:
        """
        Returns the label of the node with the given identifier.
        id[Label]
        :param identifier:
        :return label of the node:
        """
        pass

    @abstractmethod
    def get_node_neighbors_id_by_id(self, identifier) -> List[str]:
        """
        Returns the list of identifiers of the neighbors of the node with the given identifier.
        :param identifier:
        :return List of node identifiers:
        """
        pass

    @abstractmethod
    def getAllNodesId(self) -> List[str]:
        """
        Returns the list of identifiers of all nodes in the graph.
        :return List of node identifiers:
        """
        pass
    
    @abstractmethod
    def get_edges_description(self) -> List[str]:
        """
        Returns the of edges of all nodes in the graph
        :return List of edges
        """
        pass
