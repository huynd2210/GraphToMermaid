# Example usage for a Computer Science topic graph
# TODO: Turn this into CLI tool as well as pip-installable package
from adapter.DefaultGraph import DefaultGraph
from adapter.MermaidAdapter import mermaid_to_graph, graph_to_mermaid
import time

mermaid_code = """
  flowchart TB
    A[alibaba]
    A ==>|bruh| D -->|lagger| E
    S --> A
    D --> B
    G ~~~ S
    
"""

time1 = time.time()
graph = DefaultGraph()
graph = mermaid_to_graph(mermaid_code, graph)
print(graph)
print("------")
mermaid_code_from_graph = graph_to_mermaid(graph)
print(mermaid_code_from_graph)

time2 = time.time()
print(time2 - time1, "seconds")
