import unittest
from adapter.Parser import *
from mermaid_builder.mermaid_builder import Chart, ChartDir, Node, Link, NodeShape, LinkType

class testParser(unittest.TestCase):
    delimiters =  {
        ('[\\', '\\]'): NodeShape.PARALLELOGRAM_ALT,
        ('[/', '\\]'): NodeShape.TRAPEZOID,
        ('[\\', '/]'): NodeShape.TRAPEZOID_ALT,
        ('[(', ')]'): NodeShape.CYLINDER,
        ('[[', ']]'): NodeShape.SUBROUTINE,
        ('([', '])'): NodeShape.STADIUM,
        ('((', '))'): NodeShape.CIRCLE,
        ('{{', '}}'): NodeShape.HEXAGON,
        ('[/', '/]'): NodeShape.PARALLELOGRAM,
        ('>', ']'): NodeShape.ASSYMETRIC,
        ("[", "]"): NodeShape.RECT, 
        ("(", ")"): NodeShape.RECT_ROUND,
        ('{', '}'): NodeShape.RHOMBUS
    }

    mermaid_links_types = {
        r'-->(?:\|(.+?)\|)': LinkType.ARROW,
        r'-.->(?:\|(.+?)\|)': LinkType.DOTTED,
        r'==>(?:\|(.+?)\|)': LinkType.THICK,
        r'---(?:\|(.+?)\|)': LinkType.OPEN,
        r'~~~(?:\|(.+?)\|)': LinkType.INVISIBLE,
        r'--\s+(.+?)\s+-->': LinkType.ARROW,
        r'-.\s+(.+?)\s+.->': LinkType.DOTTED,
        r'==\s+(.+?)\s+==>': LinkType.THICK,
        r'--\s+(.+?)\s+---': LinkType.OPEN,
        r'~~\s+(.+?)\s+~~~': LinkType.INVISIBLE,
        r'-->': LinkType.ARROW,
        r'-.->': LinkType.DOTTED,
        r'---': LinkType.OPEN,
        r'~~~': LinkType.INVISIBLE,
        r'==>': LinkType.THICK
    }

    def testExtractNodeLabel(self):
        self.assertEqual(extractNodeLabel('A', self.delimiters), None)        
        self.assertEqual(extractNodeLabel('A(access)', self.delimiters), ('access', NodeShape.RECT_ROUND))
        self.assertEqual(extractNodeLabel('A[access]', self.delimiters), ('access', NodeShape.RECT))
        self.assertEqual(extractNodeLabel('A{access}', self.delimiters), ('access', NodeShape.RHOMBUS))
        self.assertEqual(extractNodeLabel('A>access]', self.delimiters), ('access', NodeShape.ASSYMETRIC))
        self.assertEqual(extractNodeLabel('A[/access/]', self.delimiters), ('access', NodeShape.PARALLELOGRAM))
        self.assertEqual(extractNodeLabel('A{{access}}', self.delimiters), ('access', NodeShape.HEXAGON))
        self.assertEqual(extractNodeLabel('A((access))', self.delimiters), ('access', NodeShape.CIRCLE))
        self.assertEqual(extractNodeLabel('A[[access]]', self.delimiters), ('access', NodeShape.SUBROUTINE))
        self.assertEqual(extractNodeLabel('A[(access)]', self.delimiters), ('access', NodeShape.CYLINDER))
        self.assertEqual(extractNodeLabel('A[\\access/]', self.delimiters), ('access', NodeShape.TRAPEZOID_ALT))
        self.assertEqual(extractNodeLabel('A[/access\\]', self.delimiters), ('access', NodeShape.TRAPEZOID))
        self.assertEqual(extractNodeLabel('A[\\access\\]', self.delimiters), ('access', NodeShape.PARALLELOGRAM_ALT))
 
        self.assertEqual(extractNodeLabel('A>boo]', self.delimiters), ('boo', NodeShape.ASSYMETRIC)) 
        self.assertEqual(extractNodeLabel('A[(alibaba32_32!)]', self.delimiters), ('alibaba32_32!', NodeShape.CYLINDER))

    def testExtractNodes(self):
        line = """
        flowchart TD
            A(Alibaba)
            B --> C
        """
        self.assertEqual(extractNodes(line, self.delimiters, self.mermaid_links_types),
            [('A', 'Alibaba', NodeShape.RECT_ROUND), ('B', 'B', NodeShape.RECT_ROUND), ('C', 'C', NodeShape.RECT_ROUND)])

        line = """
        flowchart TD
            B((toy))
            A --> B --> C
            D --> E
            E ~~~ F
        """
        self.assertEqual(extractNodes(line, self.delimiters, self.mermaid_links_types),
            [('B', 'toy', NodeShape.CIRCLE), ('A', 'A', NodeShape.RECT_ROUND), ('C', 'C', NodeShape.RECT_ROUND), 
                ('D', 'D', NodeShape.RECT_ROUND), ('E', 'E', NodeShape.RECT_ROUND), ('F', 'F', NodeShape.RECT_ROUND)])

        line = """
        flowchart TD
            A[[gene]]
            B((toy))
            A --> B --> C
            D --> E & C
            E ~~~ F & G 
            G & H --> L & E
        """

        self.assertEqual(extractNodes(line, self.delimiters, self.mermaid_links_types),
            [('A', 'gene', NodeShape.SUBROUTINE), ('B', 'toy', NodeShape.CIRCLE), ('C', 'C', NodeShape.RECT_ROUND), 
                ('D', 'D', NodeShape.RECT_ROUND), ('E', 'E', NodeShape.RECT_ROUND), ('F', 'F', NodeShape.RECT_ROUND),
                ('G', 'G', NodeShape.RECT_ROUND), ('H', 'H', NodeShape.RECT_ROUND), ('L', 'L', NodeShape.RECT_ROUND)])

    def testExtractNodeDeclarationFromMermaid(self):
        pass 

    def testExtractNodesFromLinks(self):
        line = """
        flowchart TD
            A(Alibaba)
            B --> C
        """
        self.assertEqual(extractNodesFromLinks(line, self.mermaid_links_types),
            ['B', 'C'])

        line = """
        flowchart TD
            B((toy))
            A --> B --> C
            D --> E
            E ~~~ F
        """
        self.assertEqual(extractNodesFromLinks(line, self.mermaid_links_types),
            ['A', 'B', 'C', 'D', 'E', 'F'])

        line = """
        flowchart TD
            A[[gene]]
            B((toy))
            A --> B --> C
            D --> E & C
            E ~~~ F & G 
            G & H --> L & E --> S
        """

        self.assertEqual(extractNodesFromLinks(line, self.mermaid_links_types),
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'L', 'S'])

    def testGetNodeFromSite(self):
        self.assertEqual(getNodeFromSite('A'), ['A']) 
        self.assertEqual(getNodeFromSite('A & B'), ['A', 'B'])  
        self.assertEqual(getNodeFromSite('A & B & C'), ['A', 'B', 'C']) 
        self.assertEqual(getNodeFromSite('A&B&C'), ['A', 'B', 'C']) 

    def testNormalizedEdge(self):
        self.assertEqual(normalizedEdge(['A', 'B'], ['C', 'D'], None), 
                         [('A', 'C', None), ('A', 'D', None), ('B', 'C', None), ('B', 'D', None)])
        self.assertEqual(normalizedEdge(['A', 'B'], ['C', 'D'], 'BRUH'), 
                         [('A', 'C', 'BRUH'), ('A', 'D', 'BRUH'), ('B', 'C', 'BRUH'), ('B', 'D', 'BRUH')])
        self.assertEqual(normalizedEdge(['A', 'B', 'C'], ['D', 'E', 'F'], 'BRUH'), 
                         [('A', 'D', 'BRUH'), ('A', 'E', 'BRUH'), ('A', 'F', 'BRUH'), 
                          ('B', 'D', 'BRUH'), ('B', 'E', 'BRUH'), ('B', 'F', 'BRUH'), 
                          ('C', 'D', 'BRUH'), ('C', 'E', 'BRUH'), ('C', 'F', 'BRUH')])

    def testExtractEdgesFromMermaidLine(self):
        line = 'A --> B --> C'
        self.assertEqual(extractEdgesFromMermaidLine(line, self.mermaid_links_types), [('A', 'B', ''), ('B', 'C', '')])

        line = 'A --> B & C'
        self.assertEqual(extractEdgesFromMermaidLine(line, self.mermaid_links_types), [('A', 'B', ''), ('A', 'C', '')])

        line = 'A & B --> C'
        self.assertEqual(extractEdgesFromMermaidLine(line, self.mermaid_links_types), [('A', 'C', ''), ('B', 'C', '')])

        line = 'A & B --> C & D'
        self.assertEqual(extractEdgesFromMermaidLine(line, self.mermaid_links_types), 
            [('A', 'C', ''), ('A', 'D', ''), ('B', 'C', ''), ('B', 'D', '')])

        line = 'A -- lag --> B' 
        self.assertEqual(extractEdgesFromMermaidLine(line, self.mermaid_links_types), 
            [('A', 'B', 'lag')])        

    def testExtractEdgeDetailFromLine(self):
        line = 'A -->|foo| B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), tuple(('-->|foo|', 'foo')))
        line = 'A -.->|foo| B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('-.->|foo|', 'foo'))
        line = 'A ==>|foo| B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('==>|foo|', 'foo'))
        line = 'A ---|foo| B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('---|foo|', 'foo'))
        line = 'A ~~~|foo| B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('~~~|foo|', 'foo'))
        line = 'A -- foo --> B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('-- foo -->', 'foo' ))
        line = 'A -. foo .-> B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('-. foo .->', 'foo' ))
        line = 'A == foo ==> B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('== foo ==>', 'foo' ))
        line = 'A -- foo --- B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('-- foo ---', 'foo' ))
        line = 'A ~~ foo ~~~ B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('~~ foo ~~~', 'foo' ))
        line = 'A --> B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('-->', ''))
        line = 'A -.-> B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('-.->', '' ))
        line = 'A --- B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('---', ''))
        line = 'A ~~~ B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('~~~', '' ))
        line = 'A ==> B'
        self.assertSequenceEqual(extractEdgeDetailFromLine(line, self.mermaid_links_types), ('==>', ''))      

if __name__ == '__main__':
    unittest.main()
