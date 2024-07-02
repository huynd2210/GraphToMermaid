"""
This interface requires 2 methods: add_node and add_edge
"""
from abc import ABC, abstractmethod


class MermaidToGraphAdapter(ABC):

    @abstractmethod
    def add_node(self, name, data=None):
        """
        Add a node to the graph
        :param name:
        :param data:
        :return:
        """
        pass


    @abstractmethod
    def add_edge(self, id1, id2):
        """
        Add an edge to the graph
        :param id1:
        :param id2:
        :return:
        """
        pass