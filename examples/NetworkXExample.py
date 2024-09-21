import networkx as nx

from adapter import MermaidAdapter
from adapter.MermaidAdapter import graph_to_mermaid

def mermaid_to_nxGraph_example() -> None:
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
    nxGraph = MermaidAdapter.mermaid_to_graph(mermaid_code, nx.Graph())

    print(nxGraph) #Output: Graph with 9 nodes and 8 edges


if __name__ == '__main__':
    nxGraph = nx.Graph()

    nxGraph.add_node(1, name="Computer Science")
    nxGraph.add_node(2, name="Algorithms")
    nxGraph.add_node(3, name="Data Structures")
    nxGraph.add_edge(1, 2)
    nxGraph.add_edge(1, 3)

    print(nxGraph)
    mermaid_code = graph_to_mermaid(nxGraph)
    print(mermaid_code)
