import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import numpy as np
import random
from input_network_xl import (
    draw_graph,
    create_graph_from_excel_6,
    plot_graphs_side_by_side,
    add_node_attributes_from_excel,
    draw_graph_pyvis,
    assign_positions_pyvis,
)
from algorithm_multi import *  # noqa: F403
from algorithm_self import *
from node_connectivity import (
    analyze_node_connectivity,
    analyze_components_input,
    find_neighboring_components,
    analyze_system_multiple,
    analyze_node_connectivity_Di,
)
from battery_model2 import Battery_Pack

excel_path = "/Users/abhishekkiran/Documents/Arch_1_DConly.xlsx"
excel_path_2 = "/Users/abhishekkiran/Documents/Test_2.xlsx"
Arch_1 = create_graph_from_excel_6(excel_path)
Arch_2 = create_graph_from_excel_6(excel_path_2)
# graph2 = create_graph_from_excel_4(excel_path)
# graph3 = create_graph_from_excel_5(excel_path)
draw_graph(Arch_1)
draw_graph(Arch_2)
#plot_graphs_side_by_side([Arch_1, Arch_2], ["Arch_1", "Arch_2"])
# draw_graph(graph2)
# draw_graph(graph3)


add_node_attributes_from_excel(Arch_1, excel_path, "Attribute")

Analyse_Cent_1 = CentralityAnalyzer(Arch_1)
#Analyse_Cent_1.top_nodes_by_centrality(Analyse_Cent_1.betweenness_centrality, top_n=3)
#Analyse_Cent_1.top_nodes_by_centrality(Analyse_Cent_1.closeness_centrality, top_n=3)

Analyse_Cent_2 = CentralityAnalyzer(Arch_2)
#Analyse_Cent_2.top_nodes_by_centrality(Analyse_Cent_2.betweenness_centrality, top_n=3)
#Analyse_Cent_2.top_nodes_by_centrality(Analyse_Cent_2.closeness_centrality, top_n=3)

centrality_data_1 = {
    "betweenness": Analyse_Cent_1.top_nodes_by_centrality(Analyse_Cent_1.betweenness_centrality, top_n=3),
    "closeness": Analyse_Cent_1.top_nodes_by_centrality(Analyse_Cent_1.closeness_centrality, top_n=3)
}

centrality_data_2 = {
    "betweenness": Analyse_Cent_2.top_nodes_by_centrality(Analyse_Cent_2.betweenness_centrality, top_n=3),
    "closeness": Analyse_Cent_2.top_nodes_by_centrality(Analyse_Cent_2.closeness_centrality, top_n=3)
}


betweenness_comparison = compare_centralities(centrality_data_1, centrality_data_2, "betweenness")
closeness_comparison = compare_centralities(centrality_data_1, centrality_data_2, "closeness")

#print_better_nodes(betweenness_comparison, "Betweenness")
print("\n")
#print_better_nodes(closeness_comparison, "Closeness")

print("Comparison of Betweenness Centrality:")
for node, val1, val2, diff in betweenness_comparison:
    print(f"Node: {node}, Arch_1: {val1}, Arch_2: {val2}, Difference: {diff}")

print("\nComparison of Closeness Centrality:")
for node, val1, val2, diff in closeness_comparison:
    print(f"Node: {node}, Arch_1: {val1}, Arch_2: {val2}, Difference: {diff}")


# Centrality_1 = Analyse_Cent.centrality_table()
# print(Centrality_1)

# Analyse_Cent_2 = CentralityAnalyzer(Arch_2)
# Analyse_Cent_2.top_nodes_by_centrality(Analyse_Cent_2.betweenness_centrality, top_n=3)
# Analyse_Cent_2.top_nodes_by_centrality(Analyse_Cent_2.closeness_centrality, top_n=3)

# Centrality_2 = Analyse_Cent_2.centrality_table()
# print(Centrality_2)

strongly_connected = nx.is_strongly_connected(Arch_1)
print("Strongly connected:", strongly_connected)
print("\n")

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


# Example data (you should replace these with your actual values)
en_density = 133  # Wh/kg
cell_capacity = 2.5  # Ah
nom_tension = 3.7  # V
sys_tension = 14.8  # V

# Example aging data (placeholder, can be adjusted as needed)
aging_data = {
    'T_store': 25,  # Storage temperature in Celsius
    'Delta_DOD': 0,  # Change in Depth of Discharge
    'V_rms': 3.7,  # RMS Voltage
    'Discharge per Cycle': 2.5,  # Discharge capacity per cycle in Ah
}

# Initialize the Battery_Pack
battery_pack = Battery_Pack(en_density, cell_capacity, nom_tension, sys_tension, aging_data)

# Step 1: Size the battery pack
battery_pack.size(
    target_dod=0.8,       # Target depth of discharge
    max_capacity=100,     # Maximum capacity in Ah
    P_points=[1000, 1200, 1500],  # Power profile in watts (example values)
    t_points=[0, 10, 20], # Time points in seconds (example values)
    verbose=True
)

# The mass of the battery pack is now calculated
battery_mass = battery_pack.mass
print(f"Battery Pack Mass: {battery_mass} kg")

battery_pack.calculate(
    P_pts=np.array([100, 200, 150, 300]),  # Power profile in watts
    t_pts=np.array([0, 1, 2, 3])          # Time points in hours 
)
# Accessing results
print("Voltage over time:", battery_pack.V)
print("Current over time:", battery_pack.I)
print("Depth of Discharge (DOD) over time:", battery_pack.DOD)
print("Open Circuit Voltage (V_OC) over time:", battery_pack.V_OC)
print("Efficiency over time:", battery_pack.eff)
