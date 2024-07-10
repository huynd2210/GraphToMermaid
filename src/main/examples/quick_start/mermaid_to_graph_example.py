from build.lib.src.main.MermaidAdapter import mermaid_to_graph
from build.lib.src.main.default_data_structures.DefaultGraph import DefaultGraph

if __name__ == '__main__':
    #Example mermaid code
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
