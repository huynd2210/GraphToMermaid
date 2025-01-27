import unittest
from adapter.Parser import extractNodeBracketStyle, extractNodes, extractEdgesFromMermaid


class TestParser(unittest.TestCase):
    def setUp(self):
        self.delimiters = {
            ("[", "]"),
            ("(", ")"),
            ('{', '}'),
            ('{{', '}}'),
            ('([', '])'),
            ('[[', ']]'),
            ('[(', ')]'),
            ('>', ']'),
            ('[/', '/]'),
            ('[\\', '\\]'),
            ('[/', '\\]'),
            ('[\\', '/]'),
            ('((', '))')
        }
        self.mermaid_links_types = {
            "-->",
            "---",
            "-.->",
            "==>",
            "~~~"
        }

    def test_extract_node_bracket_style(self):
        """Test extracting bracket styles from different node declarations"""
        test_cases = [
            ("1[Test]", "1", ("[", "]")),
            ("2(Test)", "2", ("(", ")")),
            ("3{Test}", "3", ("{", "}")),
            ("4((Test))", "4", ("((", "))")),
            ("5[[Test]]", "5", ("[[", "]]")),
        ]

        for mermaid_line, node_id, expected_brackets in test_cases:
            mermaid_code = f"flowchart TD\n{mermaid_line}"
            brackets = extractNodeBracketStyle(mermaid_code, node_id, self.delimiters)
            self.assertEqual(brackets, expected_brackets, 
                           f"Failed to extract correct brackets for {mermaid_line}")

    def test_default_bracket_style(self):
        """Test that default square brackets are returned when no style is found"""
        mermaid_code = "flowchart TD\n1 --> 2"
        brackets = extractNodeBracketStyle(mermaid_code, "1", self.delimiters)
        self.assertEqual(brackets, ("[", "]"))

    def test_extract_nodes_with_brackets(self):
        """Test that nodes are extracted with their labels correctly"""
        mermaid_code = """
        flowchart TD
        1[Node 1]
        2(Node 2)
        3{Node 3}
        1 --> 2
        2 --> 3
        """
        
        nodes = extractNodes(mermaid_code, self.delimiters, self.mermaid_links_types)
        
        self.assertEqual(nodes["1"], "Node 1")
        self.assertEqual(nodes["2"], "Node 2")
        self.assertEqual(nodes["3"], "Node 3")

    def test_extract_edges_with_different_nodes(self):
        """Test that edges are extracted correctly regardless of node bracket styles"""
        mermaid_code = """
        flowchart TD
        1[Node 1]
        2(Node 2)
        3{Node 3}
        1 --> 2
        2 --> 3
        """
        
        edges = extractEdgesFromMermaid(mermaid_code, self.mermaid_links_types)
        expected_edges = [("1", "2"), ("2", "3")]
        
        self.assertEqual(edges, expected_edges)


if __name__ == '__main__':
    unittest.main()