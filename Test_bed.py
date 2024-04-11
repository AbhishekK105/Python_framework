import networkx as nx
import matplotlib.pyplot as plt
from input_network_xl import draw_graph, create_graph_from_excel_2

excel_path = "/Users/abhishekkiran/Documents/Test_1.xlsx"
graph = create_graph_from_excel_2(excel_path)
draw_graph(graph)
