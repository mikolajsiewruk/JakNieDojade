import networkx as nx
import matplotlib.pyplot as plt
import json
import sqlite3
from Algorithms import ShortestPath


class Visualizer:
    def __init__(self):
        self.db = sqlite3.connect("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\mpk.db")
        self.cursor = self.db.cursor()

    def get_nodes_from_graph(self, graph: list, start=0, end=0) -> tuple:
        """
        Converts a graph in adjacency matrix form into a collection of connections between nodes.
        :param graph: a graph in adjacency matrix form.
        :param start: node IDs for showing the shortest path between them on the graph.
        :param end: node IDs for showing the shortest path between them on the graph.
        :returns: returns (all connections, connections in the shortest path between stops given).
        """
        sp = ShortestPath.ShortestPath()
        connections = []
        nodes_in_path = []

        if start != 0 and end != 0:
            path = sp.dijkstra(graph, start, end)[0]

            for i in range(len(path) - 1):
                nodes_in_path.append((path[i], path[i + 1]))  # add adjacent nodes from the path extracted by the algorithm to the graphs nodes

        else:
            path = []

        for j in range(len(graph)):
            for k in range(len(graph)):
                if j != k:
                    if graph[j][k] != 0:
                        connections.append((j, k))  # append connections between two nodes represented by j,k
        return connections, nodes_in_path

    def get_node_sizes(self, graph: list) -> dict:
        """
        Adjusts node sizes in a graph based on the number of possible destinations from the stop that the node represents.
        :param graph: a graph in adjacency matrix form.
        :returns: returns a dictionary of node sizes corresponding to every node index.
        """
        node_sizes = {}
        for j in range(len(graph)):
            counter = 0  # count the amount of connections from every node
            for k in range(len(graph)):
                if j != k and graph[j][k] != 0:
                    counter += 1
            if counter >= 5:  # for big nodes
                node_sizes[j] = counter * 15
            else:  # for small nodes
                node_sizes[j] = 8  # possible change
        return node_sizes

    def get_vertice_styles(self, networkx_graph: nx.Graph, connections_in_path: list) -> tuple:
        """
        Adjusts styling of networkx graph vertices for path vertices and other vertices.
        :param networkx_graph: a networkx graph class with already existing edges.
        :param connections_in_path: edges belonging to the shortest path between two nodes calculated in get_nodes_from_graph method.
        :returns: a tuple of dictionaries with vertice colors and widths
        """
        vertice_colors = {}
        vertice_width = {}

        for edge in networkx_graph.edges:
            # check if edge is in path
            # networkx doesn't allow duplicates thus also check for revers node IDs in an edge.
            if edge in connections_in_path or (edge[1], edge[0]) in connections_in_path:
                vertice_colors[edge] = 'red'  # possible changes here
                vertice_width[edge] = 5  # possible changes here
            else:
                vertice_colors[edge] = 'black'  # possible changes here
                vertice_width[edge] = 3  # possible changes here
        return vertice_colors, vertice_width

    def get_pos(self, networkx_graph: nx.Graph) -> dict:
        """
        For each node gets its coordinates from the database.
        :param networkx_graph: a networkx graph class with already existing nodes.
        :returns: a dictionary with every node's coordinates.
        """
        pos = {}
        for node in networkx_graph.nodes:
            coordinates = self.cursor.execute(f"SELECT Y,X FROM Przystanki WHERE IdP = '{node}'").fetchone()  # get nodes coordinates from the db
            pos[node] = coordinates
        return pos

    def get_labels(self, networkx_graph: nx.Graph, node_sizes: dict) -> dict:
        """
        For each node determine displayed label.
        :param networkx_graph: a networkx graph class with already existing nodes.
        :param node_sizes: a dictionary where each node ID has size assigned.
        :returns: a dictionary with custom labels for each node.
        """
        labels = {}
        for node in networkx_graph.nodes:
            if node_sizes[node] >= 75:  # check if node has more than 5 connection, terrible design needs changed
                name = self.cursor.execute(f"SELECT Nazwa FROM Przystanki WHERE IdP = '{node}'").fetchone()  # get stop's name from the db
                labels[node] = name[0]
            else:
                labels[node] = ''  # for small stops do not display any label
        return labels

    def draw_graph(self, graph: list):  # mozna zmienic to zeby bralo start i end losowo, wtedy mozna dowolna trase zaznaczyc
        """
        Draws a graph in an adjacency matrix form.
        """
        connections, connections_in_path = self.get_nodes_from_graph(graph, 10, 908)  # possible change for simulation purposes
        node_sizes = self.get_node_sizes(graph)

        G = nx.Graph()
        G.add_edges_from(connections)

        vertice_colors, vertice_width = self.get_vertice_styles(G, connections_in_path)

        pos = self.get_pos(G)
        sizes = [node_sizes[node] for node in G.nodes]
        colors = [vertice_colors[edge] for edge in G.edges]
        widths = [vertice_width[edge] for edge in G.edges]
        labels = self.get_labels(G, node_sizes)

        plt.figure(figsize=(20, 20))
        nx.draw_networkx(G, pos, node_size=sizes, edge_color=colors, width=widths, labels=labels, font_size=6,
                         font_color='red', font_weight='bold')
        plt.savefig('xd.png')


v = Visualizer()
file = open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graph.json", "r")
graph = json.load(file)
v.draw_graph(graph)
