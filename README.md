GraphToMermaid is a python library that turn any graph data structure into mermaid code and vice versa.

### Installation
Install with pip:

```
pip install GraphToMermaid
```

### Quick Start
Converting mermaid code to pre-defined graph:
```python
from adapter.MermaidAdapter import mermaid_to_graph
from adapter.DefaultGraph import DefaultGraph

mermaid_code = """
  flowchart TB
     A --> C
     A --> D
     B --> C
     B --> D
"""

graph = DefaultGraph()
graph = mermaid_to_graph(mermaid_code, graph)
print(graph)
```

Converting from graph to mermaid code:
```python
from adapter.MermaidAdapter import graph_to_mermaid
from adapter.DefaultGraph import DefaultGraph

graph = DefaultGraph()

graph.add_node("1", "Computer Science")
graph.add_node("2", "Programming")
graph.add_node("3", "Algorithms")

graph.add_edge("1", "2")
graph.add_edge("1", "3")
graph.add_edge("2", "3")

mermaid_code_from_graph = graph_to_mermaid(graph)
print(mermaid_code_from_graph)
```
