import networkx as nx
import matplotlib.pyplot as plt
import json


class Visualizer:

    def get_nodes(self, filepath):
        """
        Returns a list with connections (i,j) where i,j represent node numbers with a connection and a dictionary of node sizes where {i:number_of_connections *10}.
        """
        file = open(filepath, "r")
        g = json.load(file)
        graph = g[0]["graph"]
        connections = []
        node_size = {}

        for i in range(len(graph)):
            counter = 0
            for j in range(0, len(graph)):
                if i != j:
                    if graph[i][j] != 0:
                        counter += 1
                        connections.append((i, j))
            if counter != 0:
                node_size[i] = counter * 10

        return connections, node_size

    def graph(self, filepath):
        """
        Plots a connections graph.
        """
        connections, node_size = self.get_nodes(filepath)
        G = nx.Graph()
        G.add_edges_from(connections)
        nodes = list(G.nodes)
        pos = nx.kamada_kawai_layout(G)

        sizes = [0 for i in range(len(list(G.nodes)))]

        for k in range(len(list(G.nodes))):
            sizes[k] = node_size[nodes[k]]

        nx.draw(G, pos, node_size=sizes)
        plt.show()


v = Visualizer()
v.graph("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graph.json")