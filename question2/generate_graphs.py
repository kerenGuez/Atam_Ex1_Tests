import random
import networkx as nx
import matplotlib.pyplot as plt


def generate_random_acyclic_graph(num_nodes):
    acyclic_graph = nx.DiGraph()

    # Generate random probability for each pair of nodes
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            probability = random.random()  # Generate a random probability between 0 and 1
            if probability < 0.5:  # Adjust threshold as needed
                acyclic_graph.add_edge(i, j)  # Add edge with generated probability

    # Ensure the graph is acyclic
    while not nx.is_directed_acyclic_graph(acyclic_graph):
        # If the graph contains cycles, remove a random edge
        edge_to_remove = random.choice(list(acyclic_graph.edges()))
        acyclic_graph.remove_edge(*edge_to_remove)

    return acyclic_graph


def generate_random_cyclic_graph(num_nodes):
    # Determine a random number of edges based on the number of nodes
    min_edges = num_nodes - 1  # Minimum number of edges to form a cycle
    max_edges = num_nodes * (num_nodes - 1) // 2  # Maximum number of edges in a complete graph
    num_edges = random.randint(min_edges, max_edges)

    # Generate a random graph
    cyclic_graph = nx.gnm_random_graph(num_nodes, num_edges, directed=True)

    # Add edges until a cycle is formed
    while nx.number_of_edges(cyclic_graph) == num_edges:
        node1, node2 = random.sample(range(num_nodes), 2)
        if not cyclic_graph.has_edge(node1, node2):
            cyclic_graph.add_edge(node1, node2)
            if nx.is_directed_acyclic_graph(cyclic_graph):
                cyclic_graph.remove_edge(node1, node2)
            else:
                break

    return cyclic_graph


def generate_from_lists(nodes, edges):
    # Create an empty graph
    graph = nx.DiGraph()
    # Add nodes and edges to the graph
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph


def print_graph_info(graph):
    print("Nodes and their edges:")
    for node in graph.nodes():
        edges = graph.edges(node)
        print(f"Node {node}: Edges {edges}")


def visualize_graph(graph, file_name):
    plt.figure()  # Create a new figure for each graph visualization
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=1000, node_color='skyblue',
            font_size=10)
    plt.savefig(file_name, dpi=300)
    plt.show()


if __name__ == "__main__":
    num_nodes1 = 2
    cycle_graph1 = generate_random_acyclic_graph(num_nodes1)
    visualize_graph(cycle_graph1, "O.jpeg")
    print_graph_info(cycle_graph1)
