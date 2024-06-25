import pprint
from abc import ABC, abstractmethod
from typing import List

from mermaid_builder.flowchart import Chart, ChartDir, Node, Link

"""
This is an abstract class that defines the interface for converting a graph to a Mermaid string.`
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




def remove_string_between_delimiters(string, delimiters):
    """
    Removes the substring and delimiters from the string.

    Args:
    string (str): The input string.
    delimiters (set of tuple): A set of tuples where each tuple contains a pair of delimiters.

    Returns:
    str: The string with the substring and delimiters removed.
    """
    for delim in delimiters:
        start_delim, end_delim = delim
        if start_delim in string and end_delim in string:
            start_index = string.index(start_delim)
            end_index = string.index(end_delim, start_index) + len(end_delim)
            return string[:start_index] + string[end_index:]
    return string

def get_string_between_delimiters(text, start_delim, end_delim):
    if start_delim not in text or end_delim not in text:
        return None
    start = text.split(start_delim, 1)[1]
    return start.split(end_delim, 1)[0]

def extractStringInList_GivenListOfDelimiters(inputList, delimiters) -> List[str]:
    """
    Extracts substrings between given delimiters from a list of strings.

    Args:
    input_list (list of str): The list of input strings.
    delimiters (set of tuple): A set of tuples where each tuple contains a pair of delimiters.

    Returns:
    list of str: A list of substrings found between the delimiters.
    """
    results = []

    for string in inputList:
        for delimiter in delimiters:
            firstDelimiter, secondDelimiter = delimiter
            substring = get_string_between_delimiters(string, firstDelimiter, secondDelimiter)
            if substring is not None:
                results.append(substring)
                break
    return results

def extractNodeDeclarationFromMermaid(mermaid_code_as_list: str, delimiters) -> List[str]:
    declarations = []
    for line in mermaid_code_as_list:
        for delimiter in delimiters:
            firstDelimiter, secondDelimiter = delimiter
            if firstDelimiter in line and secondDelimiter in line:
                declarations.append(line)
    return declarations

def extractNodesFromMermaid(mermaid_code_as_list: str) -> List[str]:
    delimiters = {
        ("[", "]"),
        ("(", ")"),
        ('{', '}'),
        ('{{', '}}'),
        ('([', '])'),
        ('[[', ']]'),
        ('[(', ')]'),
        ('((', '))'),
        ('>', ']'),
        ('[/', '/]'),
        ('[\\', '\\]'),
        ('[/', '\\]'),
        ('[\\', '/]'),
        ('((', '))')
    }


    nodeLabels = extractStringInList_GivenListOfDelimiters(mermaid_code_as_list, delimiters)
    declarations = extractNodeDeclarationFromMermaid(mermaid_code_as_list, delimiters)
    nodeIds = []
    result = {}
    for line in declarations:
        nodeId = remove_string_between_delimiters(line, delimiters)
        nodeIds.append(nodeId)
    for id, label in zip(nodeIds, nodeLabels):
        result[id] = label
    return result

def mermaid_to_graph(mermaid_code: str, graph: MermaidToGraphAdapter):
    #Preprocess
    mermaid_code = mermaid_code.split("\n")
    mermaid_code = [line.strip() for line in mermaid_code]
    mermaid_code = [line for line in mermaid_code if line != ""]

def graph_to_mermaid(graph: GraphToMermaidAdapter, diagramType: str = "TD", title="") -> str:
    # mermaid_code = [diagramType]

    ChartDirection = {
        "LR": ChartDir.LR,
        "TD": ChartDir.TD,
        "TB": ChartDir.TB,
        "RL": ChartDir.RL,
        "BT": ChartDir.BT,
    }

    mermaidChart = Chart(title=title, direction=ChartDirection[diagramType])

    visited = set()

    def dfs(nodeId):
        if nodeId in visited:
            return

        visited.add(nodeId)

        mermaidNodeLabel = graph.get_node_label_by_id(nodeId)

        mermaidChart.add_node(Node(title=mermaidNodeLabel, id=nodeId))

        for neighborId in graph.get_node_neighbors_id_by_id(nodeId):
            if neighborId not in visited:
                mermaidChart.add_link(Link(src=nodeId, dest=neighborId))
                dfs(neighborId)

    # Start DFS from each unvisited node to ensure all nodes are included
    for nodeId in graph.getAllNodesId():
        if nodeId not in visited:
            dfs(nodeId)

    return mermaidChart


if __name__ == '__main__':
    mermaid_code = """
    flowchart TD
  1(Computer Science)
  4(Programming)
  2(Algorithms)
  7(Searching Algorithms)
  6(Sorting Algorithms)
  5(Databases)
  3(Data Structures)
  9(Linked Lists)
  8(Arrays)
  1 --> 4
  1 --> 2
  2 --> 7
  2 --> 6
  1 --> 5
  1 --> 3
  3 --> 9
  3 --> 8
    """

    mermaid_code_as_list = mermaid_code.split("\n")

    nodes = extractNodesFromMermaid(mermaid_code_as_list)
    pprint.pp(nodes)