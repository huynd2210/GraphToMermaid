import MermaidAdapter


class Node:
    def __init__(self, id, name, data=None):
        self.id = id
        self.name = name
        self.data = data
        self.neighbors = set()

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)
        neighbor.neighbors.add(self)

    def remove_neighbor(self, neighbor):
        self.neighbors.discard(neighbor)
        neighbor.neighbors.discard(self)


    def __repr__(self):
        return f"Node(id={self.id}, name='{self.name}', data={self.data})"


class Graph(MermaidAdapter.GraphToMermaidAdapter, MermaidAdapter.MermaidToGraphAdapter):
    def __init__(self):
        self.nodes = {}
        self.next_id = 1

    def add_node(self, name, data=None):
        node_id = self.next_id
        self.next_id += 1
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, name, data)
        return self.nodes[node_id]

    def remove_node(self, node_id):
        if node_id in self.nodes:
            node = self.nodes[node_id]
            for neighbor in list(node.neighbors):
                node.remove_neighbor(neighbor)
            del self.nodes[node_id]

    def add_edge(self, id1, id2):
        if id1 in self.nodes and id2 in self.nodes:
            node1 = self.nodes[id1]
            node2 = self.nodes[id2]
            node1.add_neighbor(node2)

    def remove_edge(self, id1, id2):
        if id1 in self.nodes and id2 in self.nodes:
            node1 = self.nodes[id1]
            node2 = self.nodes[id2]
            node1.remove_neighbor(node2)

    def get_nodes(self):
        return list(self.nodes.values())

    def get_edges(self):
        edges = set()
        for node in self.nodes.values():
            for neighbor in node.neighbors:
                edge = tuple(sorted([node.id, neighbor.id]))
                edges.add(edge)
        return list(edges)

    def get_node_by_name(self, name):
        for node in self.nodes.values():
            if node.name == name:
                return node
        return None

    def get_node_label_by_id(self, identifier):
        return self.nodes[identifier].name

    def get_node_neighbors_id_by_id(self, identifier):
        return [neighbor.id for neighbor in self.nodes[identifier].neighbors]
    def getAllNodesId(self):
        return list(self.nodes.keys())

    def __str__(self):
        result = "Graph:\n"
        for node in self.nodes.values():
            neighbors = ", ".join(str(neighbor.id) for neighbor in node.neighbors)
            result += f"Node {node.id} ('{node.name}'): {neighbors}\n"
        return result



def get_string_between_delimiters(text, start_delim, end_delim):
    if start_delim not in text or end_delim not in text:
        return None
    start = text.split(start_delim, 1)[1]
    return start.split(end_delim, 1)[0]

# Example usage for a Computer Science topic graph
if __name__ == "__main__":
    g = Graph()

    cs = g.add_node("Computer Science")
    algorithms = g.add_node("Algorithms")
    data_structures = g.add_node("Data Structures")
    programming = g.add_node("Programming")
    databases = g.add_node("Databases")

    g.add_edge(cs.id, algorithms.id)
    g.add_edge(cs.id, data_structures.id)
    g.add_edge(cs.id, programming.id)
    g.add_edge(cs.id, databases.id)

    sorting = g.add_node("Sorting Algorithms")
    searching = g.add_node("Searching Algorithms")
    g.add_edge(algorithms.id, sorting.id)
    g.add_edge(algorithms.id, searching.id)

    arrays = g.add_node("Arrays")
    linked_lists = g.add_node("Linked Lists")
    g.add_edge(data_structures.id, arrays.id)
    g.add_edge(data_structures.id, linked_lists.id)

    print(g)

    print("\nMermaid Code:")
    print(MermaidAdapter.graph_to_mermaid(g))
    print("------------")
    # print("\nGraph from Mermaid Code:")
    # testG = MermaidConverter.mermaid_to_graph(MermaidConverter.graph_to_mermaid(g))
    # print(testG)


    text = "Hello [world]!"
    start_delim = "["
    end_delim = "]"
    result = get_string_between_delimiters(text, start_delim, end_delim)
    print(result)  # Output: world