from typing import List

import networkx as nx

from adapter import MermaidAdapter


def test_mermaid_to_networkX_should_have_instance_of_nx_graph() -> None:
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
    assert isinstance(nxGraph, nx.Graph)