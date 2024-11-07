import networkx as nx
import matplotlib.pyplot as plt
import json

# Sample Requirements Input
requirements = {
    'Req1': {'description': 'System weight shall not exceed 10000 kg', 'components': ['motor', 'battery'], 'constraints': {'max_weight': 10000}},
    'Req2': {'description': 'Motor shall run at 5000 RPM', 'components': ['motor'], 'constraints': {'min_rpm': 5000}},
    'Req3': {'description': 'Battery shall provide 2000V', 'components': ['battery'], 'constraints': {'min_voltage': 2000}},
    'Req4': {'description': 'System shall operate in temperatures between -20°C and 50°C', 'components': ['motor', 'battery'], 'constraints': {'min_temp': -20, 'max_temp': 50}},
    'Req5': {'description': 'Battery capacity shall be at least 7500 mAh', 'components': ['battery'], 'constraints': {'min_capacity': 7500}},
    'Req6': {'description': 'Motor shall have a torque of at least 15000 Nm', 'components': ['motor'], 'constraints': {'min_torque': 15000}},
    'Req7': {'description': 'System noise level shall not exceed 75 dB', 'components': ['motor'], 'constraints': {'max_noise': 85}},
    'Req8': {'description': 'System shall be operational for at least 5 hours continuously', 'components': ['motor', 'battery'], 'constraints': {'min_operational_time': 5}},
    'Req9': {'description': 'Battery charging time shall not exceed 3 hours', 'components': ['battery'], 'constraints': {'max_charging_time': 3}},
    'Req10': {'description': 'Motor shall have a lifespan of at least 10,000 hours', 'components': ['motor'], 'constraints': {'min_lifespan': 10000}},
    'Req11': {'description': 'System shall be protected against water and dust (IP65 rating)', 'components': ['motor', 'battery'], 'constraints': {'min_protection_rating': 'IP65'}},
    'Req12': {'description': 'System cost shall not exceed $1500000', 'components': ['motor', 'battery'], 'constraints': {'max_cost': 1.5}},
    'Req13': {'description': 'System shall be operational at altitudes up to 10000 meters', 'components': ['motor', 'battery'], 'constraints': {'max_altitude': 10000}},
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
