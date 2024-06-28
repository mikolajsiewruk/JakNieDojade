import networkx as nx
import matplotlib.pyplot as plt
import json
import sqlite3
from Algorithms import ShortestPath
from Database.FindProject import find_project_root
from arcgis.geometry import Point, Polyline

class Visualizer:
    def __init__(self):
        project_root = find_project_root()
        self.db = sqlite3.connect(project_root / 'mpk.db')
        self.cursor = self.db.cursor()

    def get_nodes_from_graph(self, graph: list, path = []) -> tuple:
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

        if path:
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
                vertice_colors[edge] = 'purple'  # possible changes here
                vertice_width[edge] = 4  # possible changes here
            else:
                vertice_colors[edge] = 'pink'  # possible changes here
                vertice_width[edge] = 2  # possible changes here
        return vertice_colors, vertice_width

    def get_pos(self, networkx_graph: nx.Graph) -> dict:
        """
        For each node gets its coordinates from the database.
        :param networkx_graph: a networkx graph class with already existing nodes.
        :returns: a dictionary with every node's coordinates.
        """
        pos = {}
        for node in networkx_graph.nodes:
            coordinates = self.cursor.execute(f"SELECT Y,X FROM New_stops WHERE IdP = '{node}'").fetchone()  # get nodes coordinates from the db
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
                name = self.cursor.execute(f"SELECT NAME FROM New_stops WHERE IdP = '{node}'").fetchone()  # get stop's name from the db
                labels[node] = name[0]
            else:
                labels[node] = ''  # for small stops do not display any label
        return labels

    def draw_graph(self, graph: list,filename: str, path = []):  # mozna zmienic to zeby bralo start i end losowo, wtedy mozna dowolna trase zaznaczyc
        """
        Draws a graph in an adjacency matrix form.
        """
        connections, connections_in_path = self.get_nodes_from_graph(graph, path)  # possible change for simulation purposes
        node_sizes = self.get_node_sizes(graph)

        G = nx.Graph()
        G.add_edges_from(connections)

        vertice_colors, vertice_width = self.get_vertice_styles(G, connections_in_path)

        pos = self.get_pos(G)
        sizes = [node_sizes[node] for node in G.nodes]
        colors = [vertice_colors[edge] for edge in G.edges()]
        widths = [vertice_width[edge] for edge in G.edges()]
        labels = self.get_labels(G, node_sizes)

        plt.figure(figsize=(20, 20))
        nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color='grey')
        nx.draw_networkx_edges(G, pos, edge_color=colors, width=widths)
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=6, font_color='black', font_weight='bold',
                                verticalalignment='center', horizontalalignment='left',
                                bbox=dict(facecolor='white', alpha=0.4, edgecolor='none',
                                          boxstyle='round,pad=0.2'))
        plt.savefig(filename)
        plt.close()


    def map_stops(self,map):
        yx_all = self.cursor.execute("SELECT NAME,Y,X FROM New_stops").fetchall()
        for yx in yx_all:
            point = Point({'x': yx[1], 'y': yx[2]})

            simple_marker_symbol = {
                "type": "esriSMS",
                "style": "esriSMSCircle",
                "color": [0, 0, 0],  # zmienic kolory tutaj
                "outline": {"color": [255, 255, 255], "width": 1},
            }

            point_attributes = {"name": yx[0],
                                "description": "I am a point"}  # jakis pomysl na description by sie przydal

            map.draw(
                shape=point,
                symbol=simple_marker_symbol,
                attributes=point_attributes,
                popup={
                    "title": point_attributes["name"],
                    "content": point_attributes["description"],
                },
            )

    def map_path(self,map, graph, lines, start, end,version):
        sp = ShortestPath.ShortestPath()
        p = sp.dijkstra(graph, start, end)[0]
        print(sp.dijkstra(graph, start, end)[1])
        pt_route = sp.match_lines_to_path(p, lines)
        print(pt_route)
        i = 0
        paths = []
        path_temp = []
        color_codes = [
            [255, 0, 0],  # Red
            [0, 255, 0],  # Green
            [0, 0, 255],  # Blue
            [255, 255, 0],  # Yellow
            [0, 255, 255],  # Cyan
            [255, 0, 255],  # Magenta
            [192, 192, 192],  # Silver
            [128, 128, 128],  # Gray
            [128, 0, 0],  # Maroon
            [128, 128, 0],  # Olive
            [0, 128, 0],  # Dark Green
            [128, 0, 128],  # Purple
            [0, 128, 128],  # Teal
            [0, 0, 128],  # Navy
            [255, 165, 0],  # Orange
            [255, 192, 203],  # Pink
            [165, 42, 42],  # Brown
            [75, 0, 130],  # Indigo
            [255, 20, 147],  # Deep Pink
            [173, 216, 230]  # Light Blue
        ]
        for line in pt_route:
            path_temp = line[0]

            path = []
            stop_names = []
            for stops in path_temp:
                print(stops)
                name = self.cursor.execute(f"SELECT NAME FROM New_stops WHERE IdP = '{stops}'").fetchone()[0]
                yx = self.cursor.execute(f"SELECT Y,X FROM New_stops WHERE IdP = '{stops}'").fetchone()
                path.append([yx[0], yx[1]])
                stop_names.append(name)
            stop_names.reverse()
            polyline = Polyline(
                {
                    "paths": path
                }
            )

            polyline_attributes = {"name": line[1], "description": ", ".join(
                stop_names)+f"\n{version}"}  # zmienić na nazwy linii, opcjonalnie każdy fragment inną linią zaznaczyć innym kolorem

            simple_line_symbol = {
                "type": "esriSLS",
                "style": "esriSLSolid",
                "color": color_codes[i],
                "width": 2,
            }

            map.draw(
                shape=polyline,
                symbol=simple_line_symbol,
                attributes=polyline_attributes,
                popup={
                    "title": polyline_attributes["name"],
                    "content": polyline_attributes["description"],
                },
            )
            i += 1

    def map_comparison(self, map, old_graph, new_graph, start, end):
        sp = ShortestPath.ShortestPath()
        old_path = sp.dijkstra(old_graph, start, end)[0]
        new_path = sp.dijkstra(new_graph, start, end)[0]
        np = []
        op = []
        old_stop_names = []
        new_stop_names = []
        for stops in old_path:
            name = self.cursor.execute(f"SELECT Name FROM New_stops WHERE Idp = '{stops}'").fetchone()[0]
            yx = self.cursor.execute(f"SELECT Y,X FROM New_stops WHERE Idp = '{stops}'").fetchone()
            op.append([yx[0], yx[1]])
            old_stop_names.append(name)

        for stops in new_path:
            name = self.cursor.execute(f"SELECT Name FROM New_stops WHERE Idp = '{stops}'").fetchone()[0]
            yx = self.cursor.execute(f"SELECT Y,X FROM New_stops WHERE Idp = '{stops}'").fetchone()
            np.append([yx[0], yx[1]])
            new_stop_names.append(name)

        polyline1 = Polyline(
            {
                "paths": op
            }
        )

        polyline_attributes1 = {"name": 'OLD PATH', "description": ", ".join(
            old_stop_names)}  # zmienić na nazwy linii, opcjonalnie każdy fragment inną linią zaznaczyć innym kolorem

        simple_line_symbol1 = {
            "type": "esriSLS",
            "style": "esriSLSolid",
            "color": [0, 128, 128],
            "width": 2,
        }
        polyline2 = Polyline(
            {
                "paths": np
            }
        )

        polyline_attributes2 = {"name": 'NEW PATH', "description": ", ".join(
            new_stop_names)}  # zmienić na nazwy linii, opcjonalnie każdy fragment inną linią zaznaczyć innym kolorem

        simple_line_symbol2 = {
            "type": "esriSLS",
            "style": "esriSLSolid",
            "color": [75, 0, 130],
            "width": 2,
        }
        map.draw(
            shape=polyline1,
            symbol=simple_line_symbol1,
            attributes=polyline_attributes1,
            popup={
                "title": polyline_attributes1["name"],
                "content": polyline_attributes1["description"],
            },
        )

        map.draw(
            shape=polyline2,
            symbol=simple_line_symbol2,
            attributes=polyline_attributes2,
            popup={
                "title": polyline_attributes2["name"],
                "content": polyline_attributes2["description"],
            },
        )


'''v = Visualizer()
file = open("C:\\Users\\paula\\PycharmProjects\\JakNieDojade\\Dane\\graph.json", "r")
graph = json.load(file)
v.draw_graph(graph,10,908)'''