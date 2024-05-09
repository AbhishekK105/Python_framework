import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import csv
from tqdm import tqdm
import random


def create_networkx_graph_from_excel(excel_path):
    """
    Create a NetworkX graph from an Excel file containing system components and sub-components.

    Input: (Single file)
    excel_path (str): Path to the Excel file.

    Output:
    Graph
    """

    node_attr_label = "node attribute"
    edge_attr_label = "edge attribute"
    # Load data from Excel
    data = pd.read_excel(excel_path)

    # Create a NetworkX graph
    G = nx.Graph()

    node_attrs_colnames = [c for c in data.columns if node_attr_label in c]
    edge_attr_colnames = [c for c in data.columns if edge_attr_label in c]

    nodes = []

    # Iterate through the data to add edges with attributes
    for index, row in data.iterrows():
        source = row["source"]
        target = row["target"]
        node_attrs = {k: v for k, v in row.items() if k.startswith("node attribute")}
        edge_attrs = {k: v for k, v in row.items() if k.startswith("edge attribute")}

        # Add the edge with attributes
        G.add_edge(source, target, **edge_attrs)

        # Add node attributes
        G.nodes[source].update(node_attrs)
        G.nodes[target].update(node_attrs)

    return G


def assign_positions(graph):
    pos = {}
    levels = nx.dag_longest_path_length(graph) + 1
    level_height = 1.5 / (levels + 1)  # Increased spacing between levels

    for node in graph.nodes():
        ancestors = nx.ancestors(graph, node)
        x = random.random() * 4  # Spread out x positions more
        y = 1 - (len(ancestors) + 1) * level_height
        pos[node] = (x, y)

    return pos


def draw_graph(G):
    """
    Draw the NetworkX graph.

    Input:
        G (nx.Graph): NetworkX graph.
    """
    pos = assign_positions(G)  # Compute node positions

    nx.draw(
        G,
        pos,
        with_labels=True,
        font_weight="bold",
        node_size=1000,
        node_color="skyblue",
        font_size=8,
        font_color="black",
        edge_color="gray",
        linewidths=0.5,
    )

    # Draw nodes with attributes
    # node_attrs = nx.get_node_attributes(G, "node attribute")
    # nx.draw_networkx_nodes(G, pos, node_size=1000, node_color="skyblue")
    # nx.draw_networkx_labels(
    #     G, pos, labels=node_attrs, font_size=8, font_color="black", font_weight="bold"
    # )

    # Draw edges with attributes
    # edge_attrs = nx.get_edge_attributes(G, "edge attribute")
    # nx.draw_networkx_edges(G, pos, edge_color="gray", width=0.5)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_attrs, font_color="black")

    plt.show()


def plot_graphs_side_by_side(graphs, titles=None, figsize=(10, 5)):
    """
    Plot multiple NetworkX graphs side by side.

    Parameters:
        graphs (list): List of NetworkX graphs to be plotted.
        titles (list): Optional list of titles for each subplot.
        figsize (tuple): Size of the figure (width, height) in inches.
    """
    num_graphs = len(graphs)
    if titles is None:
        titles = [f"Graph {i+1}" for i in range(num_graphs)]

    # Create a figure with subplots arranged side by side
    fig, axs = plt.subplots(1, num_graphs, figsize=figsize)

    # Draw each graph in a separate subplot
    for i, (G, title) in enumerate(zip(graphs, titles)):
        nx.draw(G, ax=axs[i], with_labels=True)
        axs[i].set_title(title)

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plot
    plt.show()


def create_graph_from_excel_2(excel_path):
    # Create a NetworkX graph
    G = nx.Graph()

    # Load data from Excel
    data = pd.read_excel(excel_path)

    # Extract headers
    headers = data.columns.tolist()

    for index, row in tqdm(data.iterrows(), total=len(data)):
        source_node = row[headers[0]]
        target_node = row[headers[1]]

        if not G.has_node(source_node):
            G.add_node(source_node)
        if not G.has_node(target_node):
            G.add_node(target_node)

        if G.has_edge(source_node, target_node):
            # edge already exists, increase weight by one
            G[source_node][target_node]["weight"] += 1
        else:
            # add new edge with weight 1
            G.add_edge(source_node, target_node, weight=1)

    G_nodes = G.number_of_nodes()
    G_edges = G.number_of_edges()
    print("Nodes = ", G_nodes, " Edges = ", G_edges)

    return G


def create_graph_from_excel_3(excel_path):
    # Create a NetworkX graph
    G = nx.Graph()

    # Load data from Excel
    data = pd.read_excel(excel_path)

    # Extract headers
    headers = data.columns.tolist()

    # Set to keep track of added nodes
    added_nodes = set()

    for index, row in tqdm(data.iterrows(), total=len(data)):
        source_node = row[headers[0]]
        target_node = row[headers[1]]

        if source_node not in added_nodes:
            G.add_node(source_node)
            added_nodes.add(source_node)
        if target_node not in added_nodes:
            G.add_node(target_node)
            added_nodes.add(target_node)

        if G.has_edge(source_node, target_node):
            # edge already exists, increase weight by one
            G[source_node][target_node]["weight"] += 1
        else:
            # add new edge with weight 1
            G.add_edge(source_node, target_node, weight=1)

    G_nodes = G.number_of_nodes()
    G_edges = G.number_of_edges()
    print("Nodes = ", G_nodes, " Edges = ", G_edges)

    return G


def create_graph_from_excel_4(excel_path):
    # Create a NetworkX graph
    G = nx.Graph()

    # Load data from Excel
    data = pd.read_excel(excel_path)

    # Extract headers
    headers = data.columns.tolist()

    # Set to keep track of added nodes
    added_nodes = set()

    for index, row in tqdm(data.iterrows(), total=len(data)):
        source_node = row[headers[0]]
        target_node = row[headers[1]]

        print("Adding source node:", source_node)
        print("Adding target node:", target_node)

        if source_node not in added_nodes:
            G.add_node(source_node)
            added_nodes.add(source_node)
        if target_node not in added_nodes:
            G.add_node(target_node)
            added_nodes.add(target_node)

        if G.has_edge(source_node, target_node):
            # edge already exists, increase weight by one
            G[source_node][target_node]["weight"] += 1
        else:
            # add new edge with weight 1
            G.add_edge(source_node, target_node, weight=1)

    G_nodes = G.number_of_nodes()
    G_edges = G.number_of_edges()
    print("Nodes = ", G_nodes, " Edges = ", G_edges)

    return G


def create_graph_from_excel_5(excel_path):
    # Create a NetworkX graph
    G = nx.Graph()

    # Load data from Excel
    data = pd.read_excel(excel_path)

    # Extract headers
    headers = data.columns.tolist()

    # Set to keep track of added nodes
    added_nodes = set()

    for index, row in tqdm(data.iterrows(), total=len(data)):
        source_node = row[headers[0]]
        target_node = row[headers[1]]

        print("Adding source node:", source_node)
        print("Adding target node:", target_node)

        if source_node not in added_nodes:
            G.add_node(source_node)
            added_nodes.add(source_node)
        if target_node not in added_nodes:
            G.add_node(target_node)
            added_nodes.add(target_node)

        if G.has_edge(source_node, target_node):
            print("Edge already exists between", source_node, "and", target_node)
            # edge already exists, increase weight by one
            G[source_node][target_node]["weight"] += 1
        else:
            print("Adding edge between", source_node, "and", target_node)
            # add new edge with weight 1
            G.add_edge(source_node, target_node, weight=1)

    G_nodes = G.number_of_nodes()
    G_edges = G.number_of_edges()
    print("Nodes = ", G_nodes, " Edges = ", G_edges)

    return G


def create_graph_from_excel_6(excel_path):
    # Create a NetworkX graph
    G = nx.DiGraph()
    # in a Directed Graph, the node connectivity algorithm does not work
    # the graph has to be a simple graph for this to work
    # So are there other things that would not work if the graph was directed
    # need to analyse

    # Load data from Excel
    data = pd.read_excel(excel_path)

    # Strip whitespace from source and target columns
    # data["source"] = data["source"].str.strip()
    # data["target"] = data["target"].str.strip()

    # Extract source and target columns
    sources = data["source"].tolist()
    targets = data["target"].tolist()

    # Set to keep track of added nodes
    added_nodes = set()

    # Add nodes and edges
    for source, target in zip(sources, targets):
        if source not in added_nodes:
            G.add_node(source)
            added_nodes.add(source)
        if target not in added_nodes:
            G.add_node(target)
            added_nodes.add(target)

        # Add edge
        if G.has_edge(source, target):
            # edge already exists, increase weight by one
            G[source][target]["weight"] += 1
        else:
            # add new edge with weight 1
            G.add_edge(source, target, weight=1)

    G_nodes = G.number_of_nodes()
    G_edges = G.number_of_edges()
    # print("Sources = ", sources, " Targets = ", targets)
    print("Nodes = ", G_nodes, " Edges = ", G_edges)

    return G


def add_node_attributes_from_excel(graph, excel_file, sheet_name):
    # Read node attributes from Excel file
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Iterate over rows in the DataFrame
    for _, row in df.iterrows():
        node_name = row["node_name"]
        if node_name in graph.nodes:
            # Update node attributes with data from the DataFrame
            for column, value in row.items():
                if column != "node_name":  # Skip the 'node_name' column
                    graph.nodes[node_name][column] = value
