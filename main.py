# Example usage for a Computer Science topic graph
# TODO: Turn this into CLI tool as well as pip-installable package
import networkx as nx

from adapter.DefaultGraph import DefaultGraph
from adapter.MermaidAdapter import mermaid_to_graph, graph_to_mermaid

mermaid_code = """
  flowchart TB
    A[Alibaba]
    D[//logger//]
    A -- bruh --> D & S -->|lagger| E & B
    S --> A
    D --> B
    G ~~~ S

"""

graph = DefaultGraph()
#Should works with networkx
graph.add_node(1, "Computer Science")
graph.add_node(2, "Algorithms")
graph.add_edge(1, 2)

graph = mermaid_to_graph(mermaid_code, graph)
print(graph)
print("------")
mermaid_code_from_graph = graph_to_mermaid(graph)
print(mermaid_code_from_graph)
print('--------')
print(isinstance(graph, DefaultGraph))
