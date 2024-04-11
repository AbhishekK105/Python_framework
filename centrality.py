import networkx as nx
import pandas as pd


class CentralityAnalyzer:
    def __init__(self, graph):
        self.graph = graph

    def degree_centrality(self):
        return nx.degree_centrality(self.graph)

    def betweenness_centrality(self):
        return nx.betweenness_centrality(self.graph)

    def closeness_centrality(self):
        return nx.closeness_centrality(self.graph)

    def top_nodes_by_centrality(self, centrality_measure, top_n=3):
        centrality_scores = centrality_measure()
        sorted_nodes = sorted(
            centrality_scores.items(), key=lambda x: x[1], reverse=True
        )[:top_n]
        print(
            "Top",
            top_n,
            "Nodes by",
            centrality_measure.__name__.split("_")[0],
            "Centrality:",
        )
        for node, score in sorted_nodes:
            print(
                "Node:",
                node,
                "-",
                centrality_measure.__name__.split("_")[0],
                "Centrality:",
                score,
            )
        return sorted_nodes

    def centrality_table(self):
        degree_cent = self.degree_centrality()
        betweenness_cent = self.betweenness_centrality()
        closeness_cent = self.closeness_centrality()

        centrality_data = {
            "Node": list(self.graph.nodes()),
            "Degree Centrality": [degree_cent[node] for node in self.graph.nodes()],
            "Betweenness Centrality": [
                betweenness_cent[node] for node in self.graph.nodes()
            ],
            "Closeness Centrality": [
                closeness_cent[node] for node in self.graph.nodes()
            ],
        }

        centrality_df = pd.DataFrame(centrality_data)
        return centrality_df


# Example Usage:
if __name__ == "__main__":
    # Create a sample graph
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])

    # Initialize centrality analyzer
    analyzer = CentralityAnalyzer(G)

    # Print centrality measures in tabulated format
    analyzer.top_nodes_by_centrality(analyzer.degree_centrality)
    analyzer.top_nodes_by_centrality(analyzer.betweenness_centrality)
    analyzer.top_nodes_by_centrality(analyzer.closeness_centrality)
