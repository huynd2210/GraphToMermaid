from adapter import MermaidAdapter
from examples.CustomGraph import CustomGraph


"""
Example of usage
"""

if __name__ == '__main__':
    #Init your graph data structure
    g = CustomGraph()

    #Add your nodes
    cs = g.add_node("Computer Science")
    algorithms = g.add_node("Algorithms")
    data_structures = g.add_node("Data Structures")
    programming = g.add_node("Programming")
    databases = g.add_node("Databases")
    sorting = g.add_node("Sorting Algorithms")
    searching = g.add_node("Searching Algorithms")
    arrays = g.add_node("Arrays")
    linked_lists = g.add_node("Linked Lists")

    #Add your edges
    g.add_edge(cs.id, algorithms.id)
    g.add_edge(cs.id, data_structures.id)
    g.add_edge(cs.id, programming.id)
    g.add_edge(cs.id, databases.id)
    g.add_edge(algorithms.id, sorting.id)
    g.add_edge(algorithms.id, searching.id)
    g.add_edge(data_structures.id, arrays.id)
    g.add_edge(data_structures.id, linked_lists.id)

    print(g)

    print("\nMermaid Code:")
    print(MermaidAdapter.graph_to_mermaid(g))
    """
    Output:
    
    Mermaid Code:
    flowchart TD
      1(Computer Science)
      2(Algorithms)
      7(Searching Algorithms)
      6(Sorting Algorithms)
      4(Programming)
      3(Data Structures)
      9(Linked Lists)
      8(Arrays)
      5(Databases)
      1 --> 2
      2 --> 7
      2 --> 6
      1 --> 4
      1 --> 3
      3 --> 9
      3 --> 8
      1 --> 5
    """