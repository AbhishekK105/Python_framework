import networkx as nx
import matplotlib.pyplot as plt
import json

# Sample Requirements Input
requirements = {
    'Req1': {'description': 'System weight shall not exceed 15 kg', 'components': ['motor', 'battery'], 'constraints': {'max_weight': 15}},
    'Req2': {'description': 'Motor shall run at 5000 RPM', 'components': ['motor'], 'constraints': {'min_rpm': 5000}},
    'Req3': {'description': 'Battery shall provide 12V', 'components': ['battery'], 'constraints': {'min_voltage': 12}},
}

# Components list (could be expanded as needed)
components = ['motor', 'battery', 'aircraft', 'propeller', 'gearbox', 'converter', 'DC bus']

# Create a directed graph
G = nx.DiGraph()

# Add nodes for requirements and connect them to components and constraints
for req, details in requirements.items():
    G.add_node(req, label=details['description'], node_type='requirement')
    
    # Add edges for components
    for component in details['components']:
        G.add_node(component, node_type='component')
        G.add_edge(req, component)
    
    # Add edges for constraints
    for constraint, value in details['constraints'].items():
        constraint_label = f"{constraint}: {value}"
        G.add_node(constraint_label, node_type='constraint')
        G.add_edge(req, constraint_label)

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

# Option to export to JSON or GraphML
def export_graph(file_format='json'):
    if file_format == 'json':
        data = nx.node_link_data(G)  # JSON format
        with open('requirements_graph.json', 'w') as f:
            json.dump(data, f, indent=4)
    elif file_format == 'graphml':
        nx.write_graphml(G, 'requirements_graph.graphml')

# To export as JSON or GraphML
export_graph(file_format='json')  # or 'graphml'
