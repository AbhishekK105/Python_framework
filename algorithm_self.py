import networkx as nx
import pandas as pd
import json


class CentralityAnalyzer:
    def __init__(self, graph):
        self.graph = graph

    def degree_centrality(self):
        """
        Degree centrality measures the number of direct connections a node has.
        SE Implications: Nodes with high degree centrality can represent critical components
        in a system architecture, with high interaction or dependencies. Failures of these
        nodes may cause widespread impact.
        """
        return nx.degree_centrality(self.graph)

    def betweenness_centrality(self):
        """
        Betweenness centrality measures how often a node appears on the shortest path between other nodes.
        SE Implications: Nodes with high betweenness centrality represent potential bottlenecks or critical
        intermediaries in communication paths. Failure of these nodes can disrupt data flow, so their
        reliability should be prioritized.
        """
        return nx.betweenness_centrality(self.graph)

    def closeness_centrality(self):
        """
        Closeness centrality measures how close a node is to all other nodes in terms of shortest paths.
        SE Implications: Nodes with high closeness centrality are typically well-connected to the system
        and can quickly interact with other components. They may represent central hubs or key integrators
        within the system.
        """
        return nx.closeness_centrality(self.graph)

    def top_nodes_by_centrality(self, centrality_measure, top_n=3):
        """
        Print and return the top 'n' nodes based on a given centrality measure.
        SE Context: Identifying the most critical nodes by centrality helps in systems engineering to
        understand which components or subsystems play a key role in the architecture and might need
        better redundancy, reliability, or monitoring.
        """
        centrality_scores = centrality_measure()
        sorted_nodes = sorted(
            centrality_scores.items(), key=lambda x: x[1], reverse=True
        )[:top_n]
        print(
            f"Top {top_n} Nodes by {centrality_measure.__name__.split('_')[0].capitalize()} Centrality:\n"
        )
        for node, score in sorted_nodes:
            print(
                f"Node: {node} - {centrality_measure.__name__.split('_')[0].capitalize()} Centrality: {score:.4f}"
            )
        return sorted_nodes

    def centrality_table(self):
        """
        Generate a DataFrame containing various centrality measures for all nodes.
        SE Implications: This table provides a consolidated view of different centrality measures,
        which can be used to assess the criticality of nodes in terms of communication, fault tolerance,
        and structural importance.
        """
        degree_cent = self.degree_centrality()
        betweenness_cent = self.betweenness_centrality()
        closeness_cent = self.closeness_centrality()

        centrality_data = {
            "Node": list(self.graph.nodes()),
            "Degree Centrality": [degree_cent[node] for node in self.graph.nodes()],
            "Betweenness Centrality": [betweenness_cent[node] for node in self.graph.nodes()],
            "Closeness Centrality": [closeness_cent[node] for node in self.graph.nodes()],
        }

        centrality_df = pd.DataFrame(centrality_data)
        return centrality_df

def compare_centralities(data1, data2, metric):
    result = []
    for (node1, value1) in data1[metric]:
        matched = False
        for (node2, value2) in data2[metric]:
            if node1 == node2:
                matched = True
                result.append((node1, value1, value2, value1 - value2))
        if not matched:
            result.append((node1, value1, None, None))
    for (node2, value2) in data2[metric]:
        if node2 not in [node1 for node1, _, _, _ in result]:
            result.append((node2, None, value2, None))
    return result

def print_better_nodes(comparison, metric_name):
    print(f"Nodes where one architecture does better for {metric_name} Centrality:")
    for node, val1, val2, diff in comparison:
        if diff is not None:  # Ensure we have a valid comparison
            if diff > 0:
                print(f"Node: {node}, Arch_1: {val1} (better), Arch_2: {val2}")
            elif diff < 0:
                print(f"Node: {node}, Arch_2: {val2} (better), Arch_1: {val1}")

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




def analyze_node_connectivity(graph):
    """
    Perform node connectivity analysis and evaluate consequences of node failures in the system architecture.

    Parameters:
    - graph: NetworkX graph representing the system architecture.

    Returns:
    - critical_nodes: List of critical nodes identified based on node connectivity analysis.
    - consequences: Dictionary mapping critical nodes to their potential consequences.
    """
    # Calculate minimum node cut
    min_node_cut = nx.minimum_node_cut(graph)

    # using minimum_node_cut() function, this is defined
    # as the minimum number of nodes
    # that need to be removed to disconnect a graph. It's often used to identify
    # critical nodes in a network.

    # Identify critical nodes
    critical_nodes = list(min_node_cut)

    # Evaluate consequences of node failures
    consequences = {}

    for node in critical_nodes:
        # Determine neighbors of critical node
        neighbors = list(graph.neighbors(node))

        # Assess consequences of node failure

        consequences[node] = {
            "Neighbors": neighbors,
            "Potential Consequences": "Loss of critical function or capability",
        }

    return critical_nodes, consequences


def analyze_components_input(graph):
    """
    Analyze components and their neighboring immediate components in the system architecture.

    Parameters:
    - graph: NetworkX graph representing the system architecture.

    Returns:
    - None
    """
    # Ask user if they want to analyze components
    analyze = input("Do you want to analyze components? (yes/no): ").lower()

    if analyze == "no":
        print("Exiting...")
        return
    elif analyze != "yes":
        print("Invalid input. Please enter 'yes' or 'no'.")
        return

    # Create a dictionary to map numeric keys to component names
    component_dict = {i + 1: component for i, component in enumerate(graph.nodes())}

    # Print available components with numeric keys
    print("Available components:")
    for key, component in component_dict.items():
        print(f"{key}: {component}")

    # Ask user to select a component
    component_key = input("Enter the number of the component you want to analyze: ")
    try:
        component_key = int(component_key)
        component_name = component_dict.get(component_key)
        if component_name is None:
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter a valid component number.")
        return

    # Get neighboring immediate components
    neighbors = list(graph.neighbors(component_name))

    # Print neighboring immediate components
    print(f"Neighboring immediate components of {component_name}:")
    for neighbor in neighbors:
        print("-", neighbor)


def find_neighboring_components(graph, component_name):
    """
    Find neighboring immediate components of the specified component in the system architecture.

    Parameters:
    - graph: NetworkX graph representing the system architecture.
    - component_name: Name of the component to find neighboring immediate components for.

    Returns:
    - neighboring_components: List of neighboring immediate components of the specified component.
    """
    # Check if the component exists in the graph
    if component_name not in graph.nodes():
        print("Component not found in the system architecture.")
        return []

    # Find neighboring immediate components
    neighboring_components = list(graph.neighbors(component_name))

    return neighboring_components


def analyze_system_multiple(graphs):
    """
    Analyze systems for multiple graphs and print out the results in a tabular format.

    Parameters:
    - graphs: List of NetworkX graphs representing the system architectures.

    Returns:
    - None
    """
    # Initialize variables to track overall consequences
    min_consequences = float("inf")
    min_graph_name = None

    # Initialize DataFrame to store results
    results = []

    # Analyze systems for each graph
    for graph in graphs:
        # Analyze system for the current graph
        critical_nodes, consequences = analyze_node_connectivity(graph)

        # Calculate total consequences for the current graph
        total_consequences = sum(len(consequences[node]) for node in consequences)

        # Update minimum consequences and graph name if necessary
        if total_consequences < min_consequences:
            min_consequences = total_consequences
            min_graph_name = graph.name if hasattr(graph, "name") else "Graph"

        # Append results to DataFrame
        results.append(
            {
                "Graph": graph.name if hasattr(graph, "name") else "Graph",
                "Critical Nodes": ", ".join(critical_nodes),
                "Total Consequences": total_consequences,
            }
        )

    # Print results in tabular format
    print("System Analysis Results:")
    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    # Print graph with the least consequences
    print(
        f"\nThe graph with the least consequences is: {min_graph_name} (Total Consequences: {min_consequences})"
    )

def analyze_node_connectivity_Di(graph):
    """
    Perform node connectivity analysis and evaluate consequences of node failures in the system architecture.

    Parameters:
    - graph: NetworkX DiGraph representing the system architecture.

    Returns:
    - critical_nodes: List of critical nodes identified based on node connectivity analysis.
    - consequences: Dictionary mapping critical nodes to their potential consequences.
    """
    # Calculate minimum node cut for directed graph
    min_node_cut = nx.minimum_node_cut(graph)

    # Identify critical nodes
    critical_nodes = list(min_node_cut)

    # Evaluate consequences of node failures
    consequences = {}

    for node in critical_nodes:
        # Determine successors and predecessors of critical node
        successors = list(graph.successors(node))
        predecessors = list(graph.predecessors(node))

        # Assess consequences of node failure
        consequences[node] = {
            "Successors": successors,
            "Predecessors": predecessors,
            "Potential Consequences": "Loss of critical function or capability",
        }

    return critical_nodes, consequences

def analyze_system_multiple_Di(graphs):
    """
    Analyze systems for multiple graphs and print out the results in a tabular format.

    Parameters:
    - graphs: List of NetworkX graphs representing the system architectures.

    Returns:
    - None
    """
    # Initialize variables to track overall consequences
    min_consequences = float("inf")
    min_graph_name = None

    # Initialize DataFrame to store results
    results = []

    # Analyze systems for each graph
    for graph in graphs:
        # Analyze system for the current graph
        critical_nodes, consequences = analyze_node_connectivity(graph)

        # Calculate total consequences for the current graph
        total_consequences = sum(len(consequences[node]) for node in consequences)

        # Update minimum consequences and graph name if necessary
        if total_consequences < min_consequences:
            min_consequences = total_consequences
            min_graph_name = graph.name if hasattr(graph, "name") else "Graph"

        # Append results to DataFrame
        results.append(
            {
                "Graph": graph.name if hasattr(graph, "name") else "Graph",
                "Critical Nodes": ", ".join(critical_nodes),
                "Total Consequences": total_consequences,
            }
        )

    # Print results in tabular format
    print("System Analysis Results:")
    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    # Print graph with the least consequences
    print(
        f"\nThe graph with the least consequences is: {min_graph_name} (Total Consequences: {min_consequences})"
    )



