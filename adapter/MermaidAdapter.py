from adapter.Parser import extractNodes, extractEdgesFromMermaid
from adapter.MermaidToGraphAdapter import MermaidToGraphAdapter
from adapter.GraphToMermaidAdapter import GraphToMermaidAdapter
import networkx as nx
from mermaid_builder.mermaid_builder import Chart, ChartDir, Node, Link, NodeShape, LinkType


def resolve_add_edge(graph: MermaidToGraphAdapter | nx.Graph,
                     origin, destination, edgeDescription: str = None) -> None:
    if isinstance(graph, nx.Graph):
        graph.add_edge(origin, destination, edgeDescription=edgeDescription)
    else:
        graph.add_edge(origin, destination, edgeDescription)


def resolve_add_node(graph: MermaidToGraphAdapter | nx.Graph,
                     nodeId, nodeLabel, nodeShape=NodeShape.RECT_ROUND) -> None:
    if isinstance(graph, nx.Graph):
        graph.add_node(nodeId, label=nodeLabel, shape=nodeShape)
    else:
        graph.add_node(id=nodeId, name=nodeLabel, shape=nodeShape)


def mermaid_to_graph(mermaid_code: str, graph: MermaidToGraphAdapter |
                     nx.Graph) -> MermaidToGraphAdapter | nx.Graph:
    # Preprocess
    # Extract nodes
    #
    # links in regex

    mermaid_links_types = {
        r'-->(?:\|(.+?)\|)': LinkType.ARROW,
        r'-.->(?:\|(.+?)\|)': LinkType.DOTTED,
        r'==>(?:\|(.+?)\|)': LinkType.THICK,
        r'---(?:\|(.+?)\|)': LinkType.OPEN,
        r'~~~(?:\|(.+?)\|)': LinkType.INVISIBLE,
        r'--\s+(.+?)\s+-->': LinkType.ARROW,
        r'-.\s+(.+?)\s+.->': LinkType.DOTTED,
        r'==\s+(.+?)s+==>': LinkType.THICK,
        r'--\s+(.+?)\s+---': LinkType.OPEN,
        r'~~\s+(.+?)\s+~~~': LinkType.INVISIBLE,
        r'-->': LinkType.ARROW,
        r'-.->': LinkType.DOTTED,
        r'---': LinkType.OPEN,
        r'~~~': LinkType.INVISIBLE,
        r'==>': LinkType.THICK
    }

    delimiters = {
        ('[\\', '\\]'): NodeShape.PARALLELOGRAM_ALT,
        ('[/', '\\]'): NodeShape.TRAPEZOID,
        ('[\\', '/]'): NodeShape.TRAPEZOID_ALT,
        ('[(', ')]'): NodeShape.CYLINDER,
        ('[[', ']]'): NodeShape.SUBROUTINE,
        ('([', '])'): NodeShape.STADIUM,
        ('((', '))'): NodeShape.CIRCLE,
        ('{{', '}}'): NodeShape.HEXAGON,
        ('[/', '/]'): NodeShape.PARALLELOGRAM,
        ('>', ']'): NodeShape.ASSYMETRIC,
        ("[", "]"): NodeShape.RECT,
        ("(", ")"): NodeShape.RECT_ROUND,
        ('{', '}'): NodeShape.RHOMBUS
    }

    nodes = extractNodes(mermaid_code, delimiters, mermaid_links_types)
    edges = extractEdgesFromMermaid(mermaid_code, mermaid_links_types)

    for node in nodes:
        nodeId, nodeLabel, nodeShape = node
        resolve_add_node(graph, nodeId, nodeLabel, nodeShape)

    for edge in edges:
        origin, destination, edgeDescription = edge
        resolve_add_edge(graph, origin, destination, edgeDescription)

    return graph


def graph_to_mermaid(graph: GraphToMermaidAdapter | MermaidToGraphAdapter |
                     nx.Graph, diagramType: str = "TD", title=""):

    import adapter.DefaultGraph
    ChartDirection = {
        "LR": ChartDir.LR,
        "TD": ChartDir.TD,
        "TB": ChartDir.TB,
        "RL": ChartDir.RL,
        "BT": ChartDir.BT,
    }

    graph = adapter.DefaultGraph.Graph_factory.create_graph(graph)

    mermaidChart = Chart(title=title, direction=ChartDirection[diagramType])

    for node in graph.getAllNodesId():
        mermaidNodeLabel = graph.get_node_label_by_id(node)
        mermaidNodeShape = graph.get_node_shape_by_id(node)
        mermaidChart.add_node(
            Node(title=mermaidNodeLabel, id=node, shape=mermaidNodeShape))

        for neighbor in graph.get_node_neighbors_id_by_id(node):
            description = graph.get_edges_description(node, neighbor)
            mermaidChart.add_link(
                Link(src=node, dest=neighbor, text=description))

    return str(mermaidChart)


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

    inp = " A-- This is the text! ---B"
    firstNode = inp.split("-->")[0].strip()
    secondNode = inp.split("-->")[1].strip()
    print("firstNode: " + firstNode)
    print("secondNode: " + secondNode)
