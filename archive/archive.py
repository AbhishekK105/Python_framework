import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import csv
from tqdm import tqdm
import random
from pyvis.network import Network


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
