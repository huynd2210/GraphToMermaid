import unittest
from adapter.MermaidAdapter import *
from adapter.DefaultGraph import DefaultGraph
from mermaid_builder.flowchart import NodeShape

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
        graph.add_node('A', name='What') 
        graph.add_node('B', name='Who')
        graph.add_node('C', name='When', shape = NodeShape.CIRCLE)
        graph.add_node('D', name='How')
        graph.add_node('E', name='Why', shape = NodeShape.ASSYMETRIC)

        graph.add_edge('A', 'B', description = "straight")
        graph.add_edge('B', 'C', description = "not straight")
        graph.add_edge('A', 'C')
        graph.add_edge('C', 'D')
        graph.add_edge('C', 'E')

        mermaid_code = graph_to_mermaid(graph)
        graph = mermaid_to_graph(mermaid_code, graph)
        evaluate_result = """
            flowchart TD
                A(What) 
                B(Who)
                C((When))
                D(How)
                E>Why]
                A -->|straight| B
                B -->|not straight| C
                A --> B
                C --> D
                C --> E
        """

if __name__ == "__main__":
    unittest.main()

