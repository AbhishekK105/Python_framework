import networkx as nx
import matplotlib.pyplot as plt
from input_network_xl import (
    draw_graph,
    create_graph_from_excel_6,
    plot_graphs_side_by_side,
    add_node_attributes_from_excel,
)
from centrality import *  # noqa: F403
from algorithm_2 import graph_edit_distance
from node_connectivity import (
    analyze_node_connectivity,
    analyze_components_input,
    find_neighboring_components,
    analyze_system_multiple,
    analyze_node_connectivity_Di,
)

excel_path = "/Users/abhishekkiran/Documents/Arch_1_DConly.xlsx"
# excel_path_2 = "/Users/abhishekkiran/Documents/Test_2.xlsx"
Arch_1 = create_graph_from_excel_6(excel_path)
# Arch_2 = create_graph_from_excel_6(excel_path_2)
# graph2 = create_graph_from_excel_4(excel_path)
# graph3 = create_graph_from_excel_5(excel_path)
draw_graph(Arch_1)
# draw_graph(Arch_2)
# plot_graphs_side_by_side([Arch_1, Arch_2], ["Arch_1", "Arch_2"])
# draw_graph(graph2)
# draw_graph(graph3)

add_node_attributes_from_excel(Arch_1, excel_path, "Attribute")

Analyse_Cent = CentralityAnalyzer(Arch_1)
Analyse_Cent.top_nodes_by_centrality(Analyse_Cent.betweenness_centrality, top_n=3)
Analyse_Cent.top_nodes_by_centrality(Analyse_Cent.closeness_centrality, top_n=3)

# Centrality_1 = Analyse_Cent.centrality_table()
# print(Centrality_1)

# Analyse_Cent_2 = CentralityAnalyzer(Arch_2)
# Analyse_Cent_2.top_nodes_by_centrality(Analyse_Cent_2.betweenness_centrality, top_n=3)
# Analyse_Cent_2.top_nodes_by_centrality(Analyse_Cent_2.closeness_centrality, top_n=3)

# Centrality_2 = Analyse_Cent_2.centrality_table()
# print(Centrality_2)

strongly_connected = nx.is_strongly_connected(Arch_1)
print("Strongly connected:", strongly_connected)

# Check weak connectivity
weakly_connected = nx.is_weakly_connected(Arch_1)
print("Weakly connected:", weakly_connected)
critical_nodes, consequences = analyze_node_connectivity_Di(Arch_1)

# Print results
print("Critical Nodes:", critical_nodes)
print("Consequences of Node Failures:")
for node, details in consequences.items():
    print(f"Node: {node}")
    print(f"- Neighbors: {details['Neighbors']}")
    print(f"- Potential Consequences: {details['Potential Consequences']}")

print("Node attributes:")
for node, attrs in Arch_1.nodes(data=True):
    print(node, attrs)
# analyze_system_multiple([Arch_1, Arch_2])
