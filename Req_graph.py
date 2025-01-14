import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json

# Load data from CSV
csv_file = 'parsed_requirements.csv'  # Replace with your actual file name
df = pd.read_csv(csv_file)

# Create a directed graph
G = nx.DiGraph()

# Iterate over rows in the DataFrame to populate the graph
for _, row in df.iterrows():
    req_id = row['requirement_id']
    description = row['description']
    components = row['component'].split(', ') if pd.notna(row['component']) else []
    variable = row['variable']
    limit_type = row['limit_type']
    value = row['value']
    unit = row['unit']

    # Add requirement node
    if not G.has_node(req_id):
        G.add_node(req_id, label=description, node_type='requirement')

    # Add component nodes and edges
    for component in components:
        if not G.has_node(component):
            G.add_node(component, node_type='component')
        G.add_edge(req_id, component)

    # Add constraint nodes and edges
    if pd.notna(variable):
        constraint_label = f"{variable} ({limit_type} {value}{unit})"
        if not G.has_node(constraint_label):
            G.add_node(constraint_label, node_type='constraint')
        G.add_edge(req_id, constraint_label)

# Define colors for different node types
node_colors = []
for node in G.nodes(data=True):
    if node[1]['node_type'] == 'requirement':
        node_colors.append('green')
    elif node[1]['node_type'] == 'component':
        node_colors.append('blue')
    elif node[1]['node_type'] == 'constraint':
        node_colors.append('red')

# Visualize the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color=node_colors, font_weight='bold', node_size=3000)
plt.show()