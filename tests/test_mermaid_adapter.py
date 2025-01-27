import unittest
from adapter.DefaultGraph import DefaultGraph
from adapter.MermaidAdapter import mermaid_to_graph, graph_to_mermaid


class TestMermaidAdapter(unittest.TestCase):
    def test_bracket_style_preservation(self):
        """Test that different bracket styles are preserved in the conversion"""
        mermaid_code = """
        flowchart TD
        1[Square Brackets]
        2(Round Brackets)
        3{Curly Brackets}
        4((Double Round))
        1 --> 2
        2 --> 3
        3 --> 4
        """
        
        graph = mermaid_to_graph(mermaid_code, DefaultGraph())
        result = graph_to_mermaid(graph)
        
        # Check that each node's bracket style is preserved
        self.assertIn('1[Square Brackets]', result)
        self.assertIn('2(Round Brackets)', result)
        self.assertIn('3{Curly Brackets}', result)
        self.assertIn('4((Double Round))', result)

    def test_default_bracket_style(self):
        """Test that nodes without explicit brackets get default square brackets"""
        mermaid_code = """
        flowchart TD
        1 --> 2
        """
        
        graph = mermaid_to_graph(mermaid_code, DefaultGraph())
        result = graph_to_mermaid(graph)
        
        # Nodes should get default square brackets
        self.assertIn('1[1]', result)
        self.assertIn('2[2]', result)

    def test_mixed_bracket_styles(self):
        """Test a graph with mixed bracket styles"""
        mermaid_code = """
        flowchart TD
        1[Computer Science]
        2(Programming)
        3{Data Structures}
        1 --> 2
        2 --> 3
        """
        
        graph = mermaid_to_graph(mermaid_code, DefaultGraph())
        result = graph_to_mermaid(graph)
        
        # Check that each node's bracket style is preserved
        self.assertIn('1[Computer Science]', result)
        self.assertIn('2(Programming)', result)
        self.assertIn('3{Data Structures}', result)
        
        # Check that edges are preserved
        self.assertIn('1 --> 2', result)
        self.assertIn('2 --> 3', result)

    def test_original_issue_example(self):
        """Test the specific example from issue #9"""
        mermaid_code = """
        flowchart TD
        1[Computer Science]
        2[Algorithms]
        1 --> 2
        """
        
        graph = mermaid_to_graph(mermaid_code, DefaultGraph())
        result = graph_to_mermaid(graph)
        
        # Check that square brackets are preserved
        self.assertIn('1[Computer Science]', result)
        self.assertIn('2[Algorithms]', result)
        self.assertIn('1 --> 2', result)


if __name__ == '__main__':
    unittest.main()