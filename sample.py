import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Define your graph
G = nx.DiGraph()

# Add nodes
nodes = ["A", "B", "C", "D", "E"]
G.add_nodes_from(nodes)

# Add edges
edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "E")]
G.add_edges_from(edges)

# Step 2: Assign positions to the nodes for a top-down flow graph
pos = {"A": (0, 0), "B": (1, -1), "C": (1, 1), "D": (2, 0), "E": (3, 0)}

# Step 3: Plot the graph
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=1000,
    node_color="lightblue",
    font_size=12,
    font_weight="bold",
    arrowsize=20,
)
plt.show()
