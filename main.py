# Example usage for a Computer Science topic graph
# TODO: Turn this into CLI tool as well as pip-installable package
from adapter.DefaultGraph import DefaultGraph
from adapter.MermaidAdapter import mermaid_to_graph, graph_to_mermaid

mermaid_code = """
  flowchart TB
    A --> C
    A --> D
    B --> C
    B --> D
    B --> E
"""

graph = DefaultGraph()
graph = mermaid_to_graph(mermaid_code, graph)
print(graph)
print("------")
mermaid_code_from_graph = graph_to_mermaid(graph)
print(mermaid_code_from_graph)
