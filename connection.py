import networkx as nx
import json

# Function to load a graph from a JSON or GraphML file
def load_graph(file_path, file_format='json'):
    if file_format == 'json':
        with open(file_path, 'r') as f:
            data = json.load(f)
        return nx.node_link_graph(data)  # Load graph from JSON
    elif file_format == 'graphml':
        return nx.read_graphml(file_path)  # Load graph from GraphML
    else:
        raise ValueError("Unsupported file format. Use 'json' or 'graphml'.")

# Function to perform case-insensitive node merging between two graphs
def merge_graphs(graph1, graph2):
    combined_graph = nx.DiGraph()

    # Create a mapping for case-insensitive node matching
    node_map = {node.lower(): node for node in graph1.nodes}
    
    # Add nodes and edges from the first graph
    for node in graph1.nodes(data=True):
        combined_graph.add_node(node[0], **node[1])
    
    for edge in graph1.edges(data=True):
        combined_graph.add_edge(edge[0], edge[1], **edge[2])
    
    # Merge nodes from graph2 into graph1 (case insensitive)
    for node, attrs in graph2.nodes(data=True):
        node_lower = node.lower()
        if node_lower in node_map:
            existing_node = node_map[node_lower]
            combined_graph.nodes[existing_node].update(attrs)  # Merge attributes
        else:
            combined_graph.add_node(node, **attrs)  # Add new node
    
    # Merge edges from graph2 into the combined graph
    for edge in graph2.edges(data=True):
        node1_lower = edge[0].lower()
        node2_lower = edge[1].lower()
        
        # Match edge endpoints case-insensitively
        if node1_lower in node_map:
            edge_1 = node_map[node1_lower]
        else:
            edge_1 = edge[0]
        
        if node2_lower in node_map:
            edge_2 = node_map[node2_lower]
        else:
            edge_2 = edge[1]
        
        combined_graph.add_edge(edge_1, edge_2, **edge[2])
    
    return combined_graph

# Function to save the combined graph as JSON or GraphML
def save_graph(graph, file_path, file_format='json'):
    if file_format == 'json':
        data = nx.node_link_data(graph)  # Convert to node-link format for JSON
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    elif file_format == 'graphml':
        nx.write_graphml(graph, file_path)
    else:
        raise ValueError("Unsupported file format. Use 'json' or 'graphml'.")

# Main logic to load, merge, and save graphs
def combine_graphs(file1, file2, output_file, input_format='json', output_format='json'):
    graph1 = load_graph(file1, file_format=input_format)
    graph2 = load_graph(file2, file_format=input_format)
    
    combined_graph = merge_graphs(graph1, graph2)
    
    save_graph(combined_graph, output_file, file_format=output_format)
    print(f"Combined graph saved to {output_file} in {output_format} format.")

# Example usage
file1 = 'graph1.json'  # Input file path for first graph
file2 = 'graph2.json'  # Input file path for second graph
output_file = 'combined_graph.json'  # Output file path for the combined graph

# Combine the graphs (you can change formats as needed)
combine_graphs(file1, file2, output_file, input_format='json', output_format='json')
