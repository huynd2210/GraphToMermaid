from adapter.MermaidAdapter import mermaid_to_graph, graph_to_mermaid

# Example usage for a Computer Science topic graph
# TODO: Turn this into CLI tool as well as pip-installable package
from adapter.DefaultGraph import DefaultGraph
from adapter.Parser import extractNodes
import pprint

mermaid_code = """
  flowchart TB
    A(Test)
    E(Oof)
    A --> C
    A --> D
    B --> C
    B --> D
    B --> E
"""
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

print(extractNodes(mermaid_code, delimiters, mermaid_links_types))

print("------")

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

print(extractNodes(mermaid_code, delimiters, mermaid_links_types))


# print(extractNodesFromLinks(mermaid_code, mermaid_links_types))
#
# graph = DefaultGraph()
# graph = mermaid_to_graph(mermaid_code, graph)
# print(graph)
# print("------")
# mermaid_code_from_graph = graph_to_mermaid(graph)
# print(mermaid_code_from_graph)
