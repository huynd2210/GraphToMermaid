from adapter.MermaidAdapter import mermaid_to_graph, extractNodesFromLinks, graph_to_mermaid

# Example usage for a Computer Science topic graph
# TODO: Turn this into CLI tool as well as pip-installable package
from adapter.DefaultGraph import DefaultGraph

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
print(extractNodesFromLinks(mermaid_code, mermaid_links_types))

graph = DefaultGraph()
graph = mermaid_to_graph(mermaid_code, graph)
print(graph)
print("------")
mermaid_code_from_graph = graph_to_mermaid(graph)
print(mermaid_code_from_graph)
