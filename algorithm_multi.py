import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance
from scipy.spatial.distance import cdist

def graph_edit_distance_single_to_many(single_graph, many_graphs):
    ged_list = []

    for target_graph in many_graphs:
        # Ensure the graphs have the same number of nodes
        max_nodes = max(single_graph.number_of_nodes(), target_graph.number_of_nodes())
        single_graph_padded = nx.convert_node_labels_to_integers(
            single_graph, label_attribute="original_label", first_label=max_nodes
        )
        target_graph_padded = nx.convert_node_labels_to_integers(
            target_graph, label_attribute="original_label", first_label=max_nodes
        )

        # Compute graph edit distance
        ged = nx.algorithms.similarity.graph_edit_distance(
            single_graph_padded, target_graph_padded
        )
        ged_list.append(ged)

    return ged_list


# Create a single example graph with random node attributes and edge weights
single_graph = nx.erdos_renyi_graph(10, 0.4)
for node in single_graph.nodes:
    single_graph.nodes[node]["attribute"] = np.random.randint(1, 10)

for edge in single_graph.edges(data=True):
    edge[2]["weight"] = np.random.randint(1, 5)

# Create multiple example graphs with random node attributes, edge weights, and different structures
many_graphs = [
    nx.erdos_renyi_graph(10, 0.4),
    nx.barabasi_albert_graph(10, 2),
    nx.random_tree(10),
    nx.watts_strogatz_graph(10, 4, 0.3),
]

# Compute the graph edit distances
ged_list = graph_edit_distance_single_to_many(single_graph, many_graphs)

print("Graph Edit Distances:")
for i, ged in enumerate(ged_list):
    print(f"Graph {i + 1}: {ged}")


def visualize_graph(graph, title):
    pos = nx.spring_layout(graph)
    labels = nx.get_edge_attributes(graph, "weight")
    nx.draw(graph, pos, with_labels=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.title(title)
    plt.show()


# Visualize the single graph
visualize_graph(single_graph, "Single Graph")

# Visualize the multiple graphs
for i, graph in enumerate(many_graphs):
    visualize_graph(graph, f"Graph {i + 1}")


def graph_edit_distance(graph1, graph2, node_cost=None, edge_cost=None):
    """
    Compute the graph edit distance between two graphs.

    Parameters:
    - graph1 and graph 2
    - node_cost: Function for node cost calculation (default: absolute difference of node attributes)
    - edge_cost: Function for edge cost calculation (default: 1 for all edges)

    Returns:
    - Graph Edit Distance
    """
    if node_cost is None:
        node_cost = lambda n1, n2: (
            np.abs(n1["attribute"] - n2["attribute"])
            if "attribute" in n1 and "attribute" in n2
            else 1
        )

    if edge_cost is None:
        edge_cost = lambda e1, e2: 1

    # Convert graphs to matrices using nx.convert_matrix.to_numpy_array
    matrix1 = nx.convert_matrix.to_numpy_array(graph1)
    matrix2 = nx.convert_matrix.to_numpy_array(graph2)

    # Ensure the diagonal elements are set to zero
    np.fill_diagonal(matrix1, 0)
    np.fill_diagonal(matrix2, 0)

    # Compute cost matrices
    cost_matrix1 = np.zeros_like(matrix1)
    cost_matrix2 = np.zeros_like(matrix2)

    for i, node1 in enumerate(graph1.nodes(data=True)):
        for j, node2 in enumerate(graph2.nodes(data=True)):
            cost_matrix1[i, j] = node_cost(node1, node2)

    for i, edge1 in enumerate(graph1.edges(data=True)):
        for j, edge2 in enumerate(graph2.edges(data=True)):
            cost_matrix2[i, j] = edge_cost(edge1, edge2)

    # Use scipy's cdist to compute the pairwise distances
    pairwise_distances = cdist(cost_matrix1, cost_matrix2)

    # Ensure the diagonal elements of the pairwise distances are set to zero
    np.fill_diagonal(pairwise_distances, 0)

    # Compute the Earth Mover's Distance using scipy's wasserstein_distance function
    ged = wasserstein_distance(
        u_values=pairwise_distances.flatten(), v_values=pairwise_distances.flatten()
    )

    return ged


# Example usage:
# Create two example graphs with node attributes
# graph_a = nx.Graph([(1, 2), (2, 3)])
# graph_a.nodes[1]["attribute"] = 3
# graph_a.nodes[2]["attribute"] = 5
# graph_a.nodes[3]["attribute"] = 7

# graph_b = nx.Graph([(10, 20), (20, 30)])
# graph_b.nodes[10]["attribute"] = 2
# graph_b.nodes[20]["attribute"] = 5
# graph_b.nodes[30]["attribute"] = 8

# # Compute the graph edit distance
# ged = graph_edit_distance(graph_a, graph_b)
# print(f"Graph Edit Distance: {ged}")

# print("\n")
# print("Next comparison")
# # Graph C
# graph_c = nx.Graph([(1, 2), (2, 3), (3, 4)])
# graph_c.nodes[1]["attribute"] = 3
# graph_c.nodes[2]["attribute"] = 5
# graph_c.nodes[3]["attribute"] = 7
# graph_c.nodes[4]["attribute"] = 2

# # Graph D
# graph_d = nx.Graph([(10, 20), (20, 30), (30, 40)])
# graph_d.nodes[10]["attribute"] = 2
# graph_d.nodes[20]["attribute"] = 5
# graph_d.nodes[30]["attribute"] = 8
# graph_d.nodes[40]["attribute"] = 1

# ged_2 = graph_edit_distance(graph_a, graph_b)

# print(f"Graph Edit Distance: {ged_2}")


def graph_edit_distance_single_to_many(
    single_graph, many_graphs, node_cost=None, edge_cost=None
):
    """
    Compute the graph edit distance between a single graph and multiple graphs.

    Parameters:
    - single_graph: NetworkX graph
    - many_graphs: List of NetworkX graphs
    - node_cost: Function for node cost calculation (default: absolute difference of node attributes)
    - edge_cost: Function for edge cost calculation (default: 1 for all edges)

    Returns:
    - List of Graph Edit Distances (one for each graph in many_graphs)
    """
    if node_cost is None:
        node_cost = lambda n1, n2: np.abs(
            n1.get("attribute", 0) - n2.get("attribute", 0)
        )

    if edge_cost is None:
        edge_cost = lambda e1, e2: 1

    ged_list = []

    for target_graph in many_graphs:
        # Convert graphs to matrices
        matrix1 = nx.convert_matrix.to_numpy_array(single_graph)
        matrix2 = nx.convert_matrix.to_numpy_array(target_graph)

        # Ensure the diagonal elements are set to zero
        np.fill_diagonal(matrix1, 0)
        np.fill_diagonal(matrix2, 0)

        # Compute cost matrices
        cost_matrix1 = np.zeros((matrix1.shape[0], matrix2.shape[0]))
        cost_matrix2 = np.zeros((matrix1.shape[1], matrix2.shape[1]))

        for i, node1 in enumerate(single_graph.nodes(data=True)):
            for j, node2 in enumerate(target_graph.nodes(data=True)):
                cost_matrix1[i, j] = node_cost(node1, node2)

        for i, edge1 in enumerate(single_graph.edges(data=True)):
            for j, edge2 in enumerate(target_graph.edges(data=True)):
                cost_matrix2[i, j] = edge_cost(edge1, edge2)

        # Use scipy's cdist to compute the pairwise distances
        pairwise_distances = cdist(cost_matrix1, cost_matrix2)

        # Ensure the diagonal elements of the pairwise distances are set to zero
        np.fill_diagonal(pairwise_distances, 0)

        # Compute the Earth Mover's Distance
        ged = wasserstein_distance(
            u_values=pairwise_distances.flatten(), v_values=pairwise_distances.flatten()
        )

        ged_list.append(ged)

    return ged_list



