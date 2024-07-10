from utils import get_string_between_delimiters

# Example usage for a Computer Science topic graph
if __name__ == "__main__":

    print("------------")
    # print("\nGraph from Mermaid Code:")
    # testG = MermaidConverter.mermaid_to_graph(MermaidConverter.graph_to_mermaid(g))
    # print(testG)


    text = "Hello [world]!"
    start_delim = "["
    end_delim = "]"
    result = get_string_between_delimiters(text, start_delim, end_delim)
    print(result)  # Output: world