import networkx as nx
import pandas as pd


def create_networkx_graph_from_excel(excel_path):
    """
    Create a NetworkX graph from an Excel file containing system components and sub-components.

    Input: (Single file)
        excel_path (str): Path to the Excel file.

    Output:
        nx.Graph: NetworkX graph representing the system components and sub-components.
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

    # Iterate through the data to add nodes and edges with attributes
    for index, row in data.iterrows():
        source = row["Source"]
        target = row["Target"]

        # Add nodes with attributes
        node_attributes = {
            column_name.replace(node_attr_label, "").strip(): row[column_name]
            for column_name in node_attrs_colnames
        }

        edge_attributes = {
            column_name.replace(edge_attr_label, "").strip(): row[column_name]
            for column_name in edge_attr_colnames
        }

        if source not in nodes:
            G.add_node(source, **node_attributes)
            nodes.append(source)
        if target not in nodes:
            G.add_node(target, **node_attributes)
            nodes.append(target)

        # Add edges with attributes
        G.add_edge(source, target, **edge_attributes)

    return G
