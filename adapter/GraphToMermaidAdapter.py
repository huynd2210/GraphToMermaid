from abc import ABC, abstractmethod
from typing import List
from mermaid_builder.mermaid_builder import NodeShape

import networkx as nx

"""
This is an interface that defines the interface for converting a graph to a Mermaid string.`
"""
class GraphToMermaidAdapter(ABC):

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
    def get_edges_description(self, id1: str, id2: str) -> List[str]:
        """
        Returns the of edges of all nodes in the graph
        :return List of edges
        """
        pass

    #Optional, returns Rect_round by default
    def get_node_shape_by_id(self, identifier):
        """
        Returns the shape of the node with the given identifier.
        :param identifier:
        :return shape of the node:
        """
        return NodeShape.RECT_ROUND