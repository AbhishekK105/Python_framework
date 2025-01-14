from pyvis.network import Network
import networkx as nx


def draw_graph_pyvis(G):
    """
    Draw the NetworkX graph using pyvis.

    Input:
        G (nx.Graph): NetworkX graph.
    """
    pos = assign_positions_pyvis(G)  # Compute node positions

    # Debug 1: Check if pos is correctly computed
    if pos is None:
        print("Error: Position dictionary is None")
        return
    print("Positions:", pos)

    # Create a pyvis Network instance
    net = Network(height="1000px", width="100%", directed=True)

    # Debug 2: Check if net is initialized
    if net is None:
        print("Error: Network initialization failed")
        return

    # Add nodes and edges to the pyvis Network
    for node in G.nodes():
        if node in pos:
            x, y = pos[node]
            net.add_node(node, x=x * 100, y=y * 100)
        else:
            print(f"Warning: Position for node {node} not found")

    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    # Debug 3 : Check the network object before showing
    print("Network nodes:", net.nodes)
    print("Network edges:", net.edges)

    # Show the bloody pyvis Network
    try:
        net.show("graph.html")
        print("Network rendered successfully")
    except AttributeError as e:
        print(f"Error: {e}")


# Example usage with a simple graph
G = nx.DiGraph()
G.add_node(1)
G.add_node(2)
G.add_edge(1, 2)


def assign_positions_pyvis(G):
    # Dummy function for position assignment
    return {1: (0, 0), 2: (1, 1)}


draw_graph_pyvis(G)
