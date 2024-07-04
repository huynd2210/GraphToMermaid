import pprint
from typing import List, Set

from mermaid_builder.flowchart import Chart, ChartDir, Node, Link

from adapter.GraphToMermaidAdapter import GraphToMermaidAdapter
from adapter.MermaidToGraphAdapter import MermaidToGraphAdapter
from utils import remove_string_between_delimiters, get_string_between_delimiters, \
    extractStringInList_GivenListOfDelimiters


def extractNodeDeclarationFromMermaid(mermaid_code_as_list: List[str], delimiters) -> List[str]:
    declarations = []
    for line in mermaid_code_as_list:
        for delimiter in delimiters:
            firstDelimiter, secondDelimiter = delimiter
            if firstDelimiter in line and secondDelimiter in line:
                declarations.append(line)
    return declarations

def isLineContainsLink(line: str, mermaid_links_types: Set[str]):
    for link_type in mermaid_links_types:
        if link_type in line:
            return link_type
    return False



#TODO: Handle complex mermaid links
def extractEdgesFromMermaid(mermaidCode: str):
    mermaid_code_as_list = mermaidCode.split("\n")
    edges = []
    mermaid_links_types = {
        "-->",
        "---",
        "-.->",
        "==>",
        "~~~"
    }

    for line in mermaid_code_as_list:
        #If there is a link in the line, extract the edge (node connection)
        linkType = isLineContainsLink(line, mermaid_links_types)
        if linkType:
            edge = (line.split(linkType)[0].strip(), line.split(linkType)[1].strip())
            edges.append(edge)
    return edges


def extractNodesFromMermaid(mermaidCode: str):
    mermaid_code_as_list = mermaidCode.split("\n")
    mermaid_code_as_list = [line.strip() for line in mermaid_code_as_list if line.strip()]

    delimiters = {
        ("[", "]"),
        ("(", ")"),
        ('{', '}'),
        ('{{', '}}'),
        ('([', '])'),
        ('[[', ']]'),
        ('[(', ')]'),
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

def mermaid_to_graph(mermaid_code: str, graph: MermaidToGraphAdapter) -> MermaidToGraphAdapter:
    # Preprocess
    # Extract nodes
    nodes = extractNodesFromMermaid(mermaid_code)
    edges = extractEdgesFromMermaid(mermaid_code)

    for node in nodes.items():
        nodeId, nodeLabel = node
        graph.add_node(id=nodeId, name=nodeLabel)

    for edge in edges:
        origin, destination = edge
        graph.add_edge(origin, destination)

    return graph

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

    nodes = extractNodesFromMermaid(mermaid_code)
    pprint.pp(nodes)

    print("-_________")

    from default_data_structures.DefaultGraph import DefaultGraph

    graph = DefaultGraph()
    graph = mermaid_to_graph(mermaid_code, graph)
    print(graph)


    # inp = " A-- This is the text! ---B"
    # firstNode = inp.split("-->")[0].strip()
    # secondNode = inp.split("-->")[1].strip()
    # print("firstNode: " + firstNode)
    # print("secondNode: " + secondNode)
