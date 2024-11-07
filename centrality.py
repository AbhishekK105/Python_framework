import networkx as nx
import pandas as pd


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


# Example Usage:
if __name__ == "__main__":
    # Create a sample graph (nodes and their connections)
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])

    # Initialize centrality analyzer
    analyzer = CentralityAnalyzer(G)

    # Top nodes by centrality measures (Degree, Betweenness, Closeness)
    print("\n--- Degree Centrality Analysis ---")
    analyzer.top_nodes_by_centrality(analyzer.degree_centrality)

    print("\n--- Betweenness Centrality Analysis ---")
    analyzer.top_nodes_by_centrality(analyzer.betweenness_centrality)

    print("\n--- Closeness Centrality Analysis ---")
    analyzer.top_nodes_by_centrality(analyzer.closeness_centrality)

    # Display centrality table with all measures
    centrality_df = analyzer.centrality_table()
    print("\nCentrality Table (Degree, Betweenness, Closeness):")
    print(centrality_df)
