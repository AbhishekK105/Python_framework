import networkx as nx
import random
from pyvis.network import Network


def assign_positions_pyvis(graph):
    pos = {}
    levels = nx.dag_longest_path_length(graph) + 1
    level_height = 1.5 / (levels + 1)  # Increased spacing between levels

    for node in graph.nodes():
        ancestors = nx.ancestors(graph, node)
        x = random.random() * 4  # Spread out x positions more
        y = 1 - (len(ancestors) + 1) * level_height
        pos[node] = (x, y)

    return pos


def draw_graph_pyvis(G):
    """
    Draw the NetworkX graph using pyvis.

    Input:
        G (nx.Graph): NetworkX graph.
    """
    pos = assign_positions_pyvis(G)  # Compute node positions

    # Create a pyvis Network instance
    net = Network(height="1000px", width="100%", directed=True)

    # Add nodes and edges to the pyvis Network
    for node in G.nodes():
        x, y = pos[node]
        net.add_node(node, x=x * 100, y=y * 100)

    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    try:
        # Show the pyvis Network
        net.show("graph.html")
    except AttributeError as e:
        print("An error occurred: ", e)
        print("This might be related to template rendering issues in pyvis.")
        # Additional debug information
        print("Network object:", net)
        print("Network object HTML attribute:", net.html)


# Example usage:
if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
    draw_graph_pyvis(G)