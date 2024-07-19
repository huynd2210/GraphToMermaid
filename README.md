GraphToMermaid is a python library that turn any graph data structure into mermaid code and vice versa.

### Installation
Install with pip:

```
pip install GraphToMermaid
```

### Quick Start
```python
from default_data_structures.DefaultGraph import DefaultGraph

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
