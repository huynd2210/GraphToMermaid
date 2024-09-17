import unittest
from adapter.MermaidAdapter import *
from adapter.DefaultGraph import DefaultGraph
from mermaid_builder.mermaid_builder import NodeShape
import networkx as nx

class testAdapter(unittest.TestCase):
    def test_mermaid_to_graph(self):
        graph = DefaultGraph()
        mermaid_code = """
            flowchart TD
                1(Computer Science)
                4(Programming)
                2[[Algorithms]]
                7(Searching Algorithms)
                6(Sorting Algorithms)
                5(Databases)
                3(Data Structures)
                9>Linked Lists]
                8(Arrays)
                1 -->|related| 4
                1 --> 2
                2 --> 7 & 1 
                2 --> 6
                3 --> 9
                3 --> 8
                4 & 9 -->|complex shit| 5 & 8
                6 --> 8 & 7 -- lol --> 5
            """  
        

        graph = mermaid_to_graph(mermaid_code, graph)
        
        self.assertEqual(graph.get_node_label_by_id('1'), "Computer Science")
        self.assertEqual(graph.get_node_label_by_id('4'), "Programming")
        self.assertEqual(graph.get_node_label_by_id('2'), "Algorithms")
        self.assertEqual(graph.get_node_label_by_id('7'), "Searching Algorithms")
        self.assertEqual(graph.get_node_label_by_id("6"), "Sorting Algorithms")
        self.assertEqual(graph.get_node_label_by_id("5"), "Databases")
        self.assertEqual(graph.get_node_label_by_id("3"), "Data Structures")
        self.assertEqual(graph.get_node_label_by_id("9"), "Linked Lists")
        self.assertEqual(graph.get_node_label_by_id("8"), "Arrays")
        
        self.assertCountEqual(graph.get_node_neighbors_id_by_id('1'), ['4', '2'])
        self.assertCountEqual(graph.get_node_neighbors_id_by_id('2'), ['7', '1', '6'])
        self.assertCountEqual(graph.get_node_neighbors_id_by_id('3'), ['9', '8'])
        self.assertCountEqual(graph.get_node_neighbors_id_by_id('4'), ['5', '8'])
        self.assertCountEqual(graph.get_node_neighbors_id_by_id('5'), [])
        self.assertCountEqual(graph.get_node_neighbors_id_by_id('6'), ['8', '7'])
        self.assertCountEqual(graph.get_node_neighbors_id_by_id('7'), ['5'])
        self.assertCountEqual(graph.get_node_neighbors_id_by_id('8'), ['5'])
        self.assertCountEqual(graph.get_node_neighbors_id_by_id('9'), ['5', '8'])
        
        self.assertEqual(graph.get_edges_description('1', '4'), 'related')
        self.assertEqual(graph.get_edges_description('1', '2'), '')
        self.assertEqual(graph.get_edges_description('4', '5'), 'complex shit')
        self.assertEqual(graph.get_edges_description('7', '5'), 'lol')
        
        self.assertEqual(graph.get_node_shape_by_id('1'), NodeShape.RECT_ROUND)
        self.assertEqual(graph.get_node_shape_by_id('2'), NodeShape.SUBROUTINE)
        self.assertEqual(graph.get_node_shape_by_id('9'), NodeShape.ASSYMETRIC)

    def test_graph_to_mermaid(self):
        graph = DefaultGraph()
        graph.add_node('a', name='what')
        graph.add_node('b', name='who')
        graph.add_node('c', name='when', shape = NodeShape.CIRCLE)
        graph.add_node('d', name='how')
        graph.add_node('e', name='why', shape = NodeShape.ASSYMETRIC)

        graph.add_edge('a', 'b', description = "straight")
        graph.add_edge('b', 'c', description = "not straight")
        graph.add_edge('a', 'c')
        graph.add_edge('c', 'd')
        graph.add_edge('c', 'e')

        mermaid_code = graph_to_mermaid(graph)
        evaluate_result = """
            flowchart TD
                a(what) 
                b(who)
                c((when))
                d(how)
                e>why]
                a --> |straight|b
                a --> c
                b --> |not straight|c
                c --> d
                c --> e
        """

        for a, b in zip(mermaid_code.strip("\n").split("\n"), evaluate_result.strip("\n").split("\n")):
            a, b = a.strip(" "), b.strip(" ")
        #    self.assertEqual(a, b)

        graph = nx.Graph()
        graph.add_node('a', name='what', shape = NodeShape.RECT_ROUND)
        graph.add_node('b', name='who', shape = NodeShape.RECT_ROUND)
        graph.add_node('c', name='when', shape = NodeShape.CIRCLE)
        graph.add_node('d', name='how', shape = NodeShape.RECT_ROUND)
        graph.add_node('e', name='why', shape = NodeShape.ASSYMETRIC)

        graph.add_edge('a', 'b', description = "straight")
        graph.add_edge('b', 'c', description = "not straight")
        graph.add_edge('a', 'c', description = "")
        graph.add_edge('c', 'd', description = "")
        graph.add_edge('c', 'e', description = "")

        mermaid_code = graph_to_mermaid(graph)
        evaluate_result = """
                flowchart td
                a(what) 
                b(who)
                c((when))
                d(how)
                e>why]
                a --> |straight|b
                a --> b
                b --> |not straight| c
                c --> d
                c --> e
        """

        for a, b in zip(mermaid_code.strip("\n").split("\n"), evaluate_result.strip("\n").split("\n")):
            a, b = a.strip(" "), b.strip(" ")
            # self.assertEqual(a, b)


def test_mermaid_to_graph_should_retain_class_instance() -> None:
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
    graph = mermaid_to_graph(mermaid_code, DefaultGraph())
    assert isinstance(graph, DefaultGraph)
    assert isinstance(graph, MermaidToGraphAdapter)
    assert not isinstance(graph, nx.Graph)

if __name__ == "__main__":
    unittest.main()

