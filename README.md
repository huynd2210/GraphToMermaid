GraphToMermaid is a python library that turn any graph data structure into mermaid code and vice versa.

### Installation
Install with pip:

```
pip install GraphToMermaid
```

### Quick Start
GraphToMermaid offers a pre-defined graph implementation (DefaultGraph) that works out of the box. 
Note: DefaultGraph uses NetworkX graph implementation.
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

### Converting from custom graph data structure
GraphToMermaid supports converting from any custom graph data structures.
Simply inherits ```MermaidToGraphAdapter``` and implements required methods in order to convert mermaid code to graph.
And ```GraphToMermaidAdapter``` for converting from graph to mermaid.

Example for a custom graph:
```python
class CustomGraph(MermaidAdapter.GraphToMermaidAdapter, MermaidAdapter.MermaidToGraphAdapter):
    def __init__(self):
        self.nodeCollection = {}
        self.next_id = 1

    def add_node(self, name, data=None):
        node_id = self.next_id
        self.next_id += 1
        if node_id not in self.nodeCollection:
            self.nodeCollection[node_id] = CustomNode(node_id, name, data)
        return self.nodeCollection[node_id]

    def remove_node(self, node_id):
        if node_id in self.nodeCollection:
            node = self.nodeCollection[node_id]
            for neighbor in list(node.neighbors):
                node.remove_neighbor(neighbor)
            del self.nodeCollection[node_id]

    def add_edge(self, id1, id2):
        if id1 in self.nodeCollection and id2 in self.nodeCollection:
            node1 = self.nodeCollection[id1]
            node2 = self.nodeCollection[id2]
            node1.add_neighbor(node2)

    def remove_edge(self, id1, id2):
        if id1 in self.nodeCollection and id2 in self.nodeCollection:
            node1 = self.nodeCollection[id1]
            node2 = self.nodeCollection[id2]
            node1.remove_neighbor(node2)

    def get_nodes(self):
        return list(self.nodeCollection.values())

    def get_edges(self):
        edges = set()
        for node in self.nodeCollection.values():
            for neighbor in node.neighbors:
                edge = tuple(sorted([node.id, neighbor.id]))
                edges.add(edge)
        return list(edges)

    def get_node_by_name(self, name):
        for node in self.nodeCollection.values():
            if node.name == name:
                return node
        return None

    def get_node_label_by_id(self, identifier):
        return self.nodeCollection[identifier].name

    def get_node_neighbors_id_by_id(self, identifier):
        return [neighbor.id for neighbor in self.nodeCollection[identifier].neighbors]
    def getAllNodesId(self):
        return list(self.nodeCollection.keys())

    def __str__(self):
        result = "Graph:\n"
        for node in self.nodeCollection.values():
            neighbors = ", ".join(str(neighbor.id) for neighbor in node.neighbors)
            result += f"Node {node.id} ('{node.name}'): {neighbors}\n"
        return result
```

See ``examples`` folder for more

