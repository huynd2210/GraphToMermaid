import pprint
from typing import List, Set

from mermaid_builder.flowchart import Chart, ChartDir, Node, Link

from adapter.GraphToMermaidAdapter import GraphToMermaidAdapter
from adapter.MermaidToGraphAdapter import MermaidToGraphAdapter
from adapter.Parser import extractNodes, isLineContainsLink, extractEdgesFromMermaid


def mermaid_to_graph(mermaid_code: str, graph: MermaidToGraphAdapter) -> MermaidToGraphAdapter:
    # Preprocess
    # Extract nodes
    mermaid_links_types = {
        "-->",
        "---",
        "-.->",
        "==>",
        "~~~"
    }

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

    nodes = extractNodes(mermaid_code, delimiters, mermaid_links_types)
    edges = extractEdgesFromMermaid(mermaid_code, mermaid_links_types)

    for node in nodes.items():
        nodeId, nodeLabel = node
        graph.add_node(id=nodeId, name=nodeLabel)

    for edge in edges:
        origin, destination = edge
        graph.add_edge(origin, destination)

    return graph


def graph_to_mermaid(graph: GraphToMermaidAdapter, diagramType: str = "TD", title=""):
    ChartDirection = {
        "LR": ChartDir.LR,
        "TD": ChartDir.TD,
        "TB": ChartDir.TB,
        "RL": ChartDir.RL,
        "BT": ChartDir.BT,
    }

    mermaidChart = Chart(title=title, direction=ChartDirection[diagramType])

    for node in graph.getAllNodesId():
        mermaidNodeLabel = graph.get_node_label_by_id(node)
        mermaidChart.add_node(Node(title=mermaidNodeLabel, id=node))

        for neighbor in graph.get_node_neighbors_id_by_id(node):
            mermaidChart.add_link(Link(src=node, dest=neighbor))

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
            1 --> 5
            1 --> 3
            2 --> 7
            2 --> 6
            3 --> 9
            3 --> 8
    """


    print("-_________")

    from adapter.DefaultGraph import DefaultGraph

    graph = DefaultGraph()
    graph = mermaid_to_graph(mermaid_code, graph)
    print("Printing graph from mermaid code")
    print(graph)
    print("-----")
    print("Printing mermaid code from graph")
    mermaid_code_from_graph = graph_to_mermaid(graph)
    print(mermaid_code_from_graph)


    # inp = " A-- This is the text! ---B"
    # firstNode = inp.split("-->")[0].strip()
    # secondNode = inp.split("-->")[1].strip()
    # print("firstNode: " + firstNode)
    # print("secondNode: " + secondNode)
