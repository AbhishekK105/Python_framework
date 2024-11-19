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

# Define dictionary for variable keywords and limit keywords
variable_keywords = {
    'weight': 'weight',
    'rpm': 'rpm',
    'voltage': 'voltage',
    'temp': 'temperature',
    # Add more variables as necessary
}

limit_keywords = {
    'max': 'upper',
    'min': 'lower'
}

# Create a directed graph
G = nx.DiGraph()

# Function to classify constraint limits and add nodes and edges
def add_constraints(req, constraints):
    for constraint, value in constraints.items():
        # Split constraint to identify possible variable and limit type
        parts = constraint.split('_')
        
        # Identify variable and limit direction from parts
        variable = next((variable_keywords.get(p) for p in parts if p in variable_keywords), None)
        limit_type = next((limit_keywords.get(p) for p in parts if p in limit_keywords), None)

        if variable and limit_type:
            # Add variable node if it doesn't exist
            if not G.has_node(variable):
                G.add_node(variable, node_type='variable')
            
            # Add numerical value node
            value_node = f"{variable}_{limit_type}_value"
            G.add_node(value_node, node_type='value', value=value)  # Store the actual value here
            
            # Create edges: requirement -> variable, variable -> value
            G.add_edge(req, variable, relation="requires")
            G.add_edge(variable, value_node, relation=limit_type)

# Add nodes for requirements and connect them to components and constraints
for req, details in requirements.items():
    G.add_node(req, label=details['description'], node_type='requirement')
    
    # Add edges for components
    for component in details['components']:
        if not G.has_node(component):
            G.add_node(component, node_type='component')
        G.add_edge(req, component, relation="includes")
    
    # Parse and add constraint edges with limits
    add_constraints(req, details['constraints'])

# Define colors for different node types
node_colors = []
for node in G.nodes(data=True):
    if node[1]['node_type'] == 'requirement':
        node_colors.append('green')
    elif node[1]['node_type'] == 'component':
        node_colors.append('blue')
    elif node[1]['node_type'] == 'variable':
        node_colors.append('orange')
    elif node[1]['node_type'] == 'value':
        node_colors.append('purple')

# Visualize the graph with edge labels to show relations
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color=node_colors, font_weight='bold', node_size=3000)
edge_labels = {(u, v): d['relation'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()

# Function to retrieve and modify numerical values
def get_value(variable, limit_type):
    value_node = f"{variable}_{limit_type}_value"
    return G.nodes[value_node]['value'] if G.has_node(value_node) else None

def set_value(variable, limit_type, new_value):
    value_node = f"{variable}_{limit_type}_value"
    if G.has_node(value_node):
        G.nodes[value_node]['value'] = new_value
    else:
        print(f"Node {value_node} does not exist.")

# Example of retrieving and modifying values
print("Original weight upper limit:", get_value("weight", "upper"))
set_value("weight", "upper", 12000)
print("Updated weight upper limit:", get_value("weight", "upper"))

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
