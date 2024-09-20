import networkx as nx
import pandas as pd


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



# Example usage:
if __name__ == "__main__":
    # Create a sample graph representing the system architecture
    G = nx.Graph()
    G.add_edges_from(
        [
            ("Power Distribution Unit", "Generator"),
            ("Generator", "Avionics System"),
            ("Generator", "Control Surfaces"),
            ("Avionics System", "Flight Control System"),
            ("Control Surfaces", "Flight Control System"),
        ]
    )

    critical_nodes, consequences = analyze_node_connectivity(G)

    # Print results
    print("Critical Nodes:", critical_nodes)
    print("Consequences of Node Failures:")
    for node, details in consequences.items():
        print(f"Node: {node}")
        print(f"- Neighbors: {details['Neighbors']}")
        print(f"- Potential Consequences: {details['Potential Consequences']}")

    # Analyze components
    analyze_components_input(G)

    # Get component name from the user
    component_name = input("Enter the name of the component you want to analyze: ")

    # Find neighboring immediate components of the specified component
    neighboring_components = find_neighboring_components(G, component_name)

    # Print neighboring immediate components
    print(f"Neighboring immediate components of {component_name}:")
    for neighbor in neighboring_components:
        print("-", neighbor)
