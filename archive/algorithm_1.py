import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


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
