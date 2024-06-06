import json
import time as tm
import numpy as np
import sqlite3
import logging
from Database.FindProject import find_project_root

logging.basicConfig(filename='line_matching.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ShortestPath:
    def __init__(self):
        project = find_project_root()
        self.db = sqlite3.connect(project/"mpk.db")
        self.cursor = self.db.cursor()

    @staticmethod
    def dijkstra(graph: list, start: int, end: int) -> tuple:
        """
        Dijkstra's algorithm for finding the shortest path in a graph.
        :param graph: a graph of nodes in adjacency matrix form
        :param start: source
        :param end: target
        :return: list of shortest distances from node 0 to the last node
        """

        # noinspection PyTypeChecker
        def reconstruct(distances: list, start: int, end: int) -> list:
            """
            Dijkstra helper function. From a given list of shortest connections returns full path.
            :param distances: List of dictionaries containing node number ("node") and list of [from which node,total distance] ("val")
            :param start: source
            :param end: target
            :return: reconstructed path
            """
            path = []
            curr = distances[end]  # set the pointer at the last node of the path
            while str(curr["val"][
                          0]) != '':  # from the last node add the values of "val"[0] key that keep track of the shortest path available.
                path.append(curr["node"])
                curr = distances[curr["val"][0]]
            path.append(start)
            path.reverse()
            return path

        unvisited = set()  # set containing all unvisited nodes
        reachable=[x for x in graph if x.count(0)<len(graph)] # temporary fix
        visited = []
        for j in range(len(graph)):
            unvisited.add(j)
        distances = []
        for i in range(len(graph)):
            if i == start:
                distances.append({"node": i, "val": ['', 0]})
            else:
                distances.append({"node": i, "val": ['',
                                                     'inf']})  # every node as a dictionary with "val" being an array [from which node,total distance]
        current = start
        prev=[]
        while unvisited:  # searching process will continue until it checks all the nodes
            if current not in prev:
                prev.append(current)
            neighbors = [i for i in range(len(graph[current])) if (graph[current][i] != 0 and i in unvisited)]
            for node in neighbors: # consider all neighboring nodes
                dist = distances[node]["val"][1]
                new_dist = distances[current]["val"][1] + graph[current][node]  # calculate the distance from the current node to each neighbor
                if dist == 'inf' or new_dist < dist:  # if the new path is shorter, switch
                    distances[node]["val"][1] = new_dist
                    distances[node]["val"][0] = current
            unvisited.remove(current)  # remove current node from unvisited
            if current not in visited:
                visited.append(current)
            valid = [nodes for nodes in distances if nodes["val"][1] != 'inf' and nodes["node"] in unvisited]  # consider all nodes that connect to current node and are not yet visited
            v = [nodes["val"][1] for nodes in distances if nodes["val"][1] != 'inf' and nodes["node"] in unvisited]  # take their path distances
            if not valid:
                current=visited[visited.index(current)-1]
                unvisited.add(current)
            if not valid and len(visited)==len(reachable):
                break

            for nodes in valid:  # from path distances select the one with the shortest distance
                if nodes["val"][1] == min(v):
                    current = nodes["node"]
        path = reconstruct(distances, start, end)
        length = distances[end]["val"][1]
        return path, length

    def bellman_ford(self, graph: list, start: int, end: int):
        """
        Finds the shortest path between two stops using the Bellman-Ford algorithm.

        Args:
            - graph (list[list[int]]): Adjacency matrix representation of the graph.
            - start (int): Index of the starting stop.
            - end (int): Index of the ending stop.

        Returns:
            - tuple: A tuple containing the shortest path from the starting stop to the ending stop and the total travel time.
        """

        num_stops = len(graph)  # Get the number of stops (vertices) in the graph

        # Convert the adjacency matrix to a list of edges (tuples representing [start, end, weight])
        edge_list = []
        for i in range(num_stops):
            for j in range(num_stops):
                if graph[i][j] != 0:
                    edge_list.append([i, j, graph[i][j]])  # Create an edge tuple

        # Initialize distances from the starting stop to all other stops as infinity
        distances = [float("inf")] * num_stops
        distances[start] = 0  # Set the distance to the starting stop as 0

        # Update distances by considering each edge in the graph
        for _ in range(num_stops - 1):  # Repeat the relaxation process n - 1 times
            for edge in edge_list:  # Iterate over each edge in the graph
                start_stop, end_stop, weight = edge  # Extract start, end, and weight from the edge
                if distances[start_stop] != float("inf") and distances[start_stop] + weight < distances[end_stop]:
                    distances[end_stop] = distances[start_stop] + weight  # Update the distance if it's shorter

        # Check for negative cycles in the graph
        for edge in edge_list:
            start_stop, end_stop, weight = edge
            if distances[start_stop] != float("inf") and distances[start_stop] + weight < distances[end_stop]:
                print("The transportation network contains a negative cycle")
                return [], float("inf")  # Return an empty path and infinity if a negative cycle is found

        # Reconstruct the shortest path from the ending stop to the starting stop
        path = [end]
        current_stop = end
        length = 0
        while current_stop != start:
            for edge in edge_list:
                next_stop, prev_stop, weight = edge
                if prev_stop == current_stop and distances[next_stop] == distances[current_stop] - weight:
                    path.insert(0, next_stop)  # Prepend the next stop to the path
                    length += weight  # Update the total travel time
                    current_stop = next_stop  # Move to the next stop
                    break

        return path, length  # Return the shortest path and total travel time



    def a_star(self,graph: list, start: int, goal: int) -> tuple:
        """
        A* heuristic algorithm for finding the shortest path in a graph.
        :param graph: a graph of nodes in adjacency matrix form
        :param start: start node
        :param goal: goal node
        :return: tuple containing the shortest path and total travel time
        """



        def f_value(node: list) -> float:
            """
            A* Helper function, determining the f_value of the given node.
            :param node: node which f_value will be calculated
            :return: f_value of the given node
            """
            g_value = node[2]
            h_value = (np.sqrt((node[3] - x_goal) ** 2 + (node[4] - y_goal) ** 2))*500
            print(h_value)
            f_value = g_value + h_value
            return f_value

        def reconstruct_path(closed_list: list, current: list) -> tuple:
            """
            A* helper function to reconstruct the path from start to goal.
            :param closed_list: list of all expanded nodes
            :param current: node whose parent we search for in order to reconstruct the path
            :return: tuple - [0] being the reconstructed path and [1] being the total cost of the path
            """

            path = []
            value = current[2]
            while current is not None:
                path.append(current[1])
                parent = current[0]
                current = next((node for node in closed_list if node[1] == parent), None)
            return path[::-1], value

        open_list = []
        closed_list = []
        x_start = self.cursor.execute(f"select X from Nowe_przystanki where IdP = '{start}';").fetchone()[0]
        y_start = self.cursor.execute(f"select Y from Nowe_przystanki where IdP = '{start}';").fetchone()[0]
        # THE WAY NODES IN OPEN AND CLOSED LISTS ARE STORED: [node's parent, node and node's g value, x coordinate, y coordinate]
        open_list.append([None, start, 0, x_start, y_start])
        x_goal = self.cursor.execute(f"select X from Nowe_przystanki where IdP = '{goal}';").fetchone()[0]
        y_goal = self.cursor.execute(f"select Y from Nowe_przystanki where IdP = '{goal}';").fetchone()[0]

        while len(open_list) != 0:  # executing as long as there are neighbours to nodes

            # determining the neighbour in open_list with the lowest f-value
            lowest_f = f_value(open_list[0])
            current = open_list[0]
            for node in open_list:
                if f_value(node) < lowest_f:
                    lowest_f = f_value(node)
                    current = node

            # checking whether current is goal - returning the path
            if current[1] == goal:
                closed_list.append(current)
                return reconstruct_path(closed_list, current)

            open_list.remove(current)
            closed_list.append(current)
            # for each node in the graph
            for i in range(len(graph[0])):
                # if the node is not the neighbour of current or is already in closed list, skip it
                if graph[current[1]][i] == 0 or any(element[1] == i for element in closed_list):
                    continue
                else:
                    # if the neighbour is already in open list
                    if any(element[1] == i for element in open_list):
                        neighbour_g = current[2] + graph[current[1]][i]
                        for j in range(len(open_list)):
                            if open_list[j][1] == i:
                                # If the new g value is lower than the old g value, update the neighbor’s g value and update its parent to the current node
                                if open_list[j][2] > neighbour_g:
                                    x = self.cursor.execute(f"select X from Nowe_przystanki where IdP = '{open_list[j][1]}';").fetchone()[0]
                                    y = self.cursor.execute(f"select Y from Nowe_przystanki where IdP = '{open_list[j][1]}';").fetchone()[0]
                                    open_list[j] = [current[1], i, neighbour_g, x, y]

                    # if the neighbour is not in the open list, add it to open list
                    else:
                        neighbour_g = current[2] + graph[current[1]][i]
                        x = self.cursor.execute(f"select X from Nowe_przystanki where IdP = '{i}';").fetchone()[0]
                        y = self.cursor.execute(f"select Y from Nowe_przystanki where IdP = '{i}';").fetchone()[0]
                        open_list.append([current[1], i, neighbour_g, x, y])

        # if the open list is empty and path has not been determined: no path possible, return false
        return ([], )

    def timer(self,graph:list,start:int,end:int)->tuple:
        """
        Returns time of searching the shortest path with Dijkstra's algorithm and Bellman-Ford algorithm.
        """
        start_d = tm.perf_counter_ns()
        self.dijkstra(graph,start,end)
        end_d = tm.perf_counter_ns()

        start_bf = tm.perf_counter_ns()
        self.bellman_ford(graph,start,end)
        end_bf = tm.perf_counter_ns()

        return end_d-start_d, end_bf-start_bf

    def match_lines_to_path(self, path: list, lines: list) -> list:
        """
        Matches public transportation lines to a path.
        :param path: a path represented by a list with numbers of nodes in a graph.
        :param lines: a list of public transportation lines represented by dictionaries.
        :returns: returns a list of tuples [(stops, line)]
        """

        def find_matching_subsequence(list1, list2) -> list:
            """
            Helper function for finding a subsequence starting in the first node of list1
            """
            first_element = list1[0]
            list2 = list(dict.fromkeys(list2))  # remove duplicates from the list to prevent bugs

            # Check if there are no subsequences
            try:
                start_index = list2.index(first_element)
            except ValueError:
                return []

            # Check if list1 is a subsequence starting from this index in list2
            if list2[start_index:start_index + len(list1)] == list1:
                return list2[start_index:start_index + len(list1)]

            longest_subsequence = []
            for i in range(len(list1)):
                # Check for the longest subsequence if starting index is in list2
                if start_index + i < len(list2) and list1[i] == list2[start_index + i]:
                    longest_subsequence.append(list1[i])
                else:
                    break

            return longest_subsequence

        route = []
        path_temp = path.copy()

        logging.info(f"Starting match_lines_to_path with path: {path}")

        # Loop over path removing stops
        while len(path_temp) > 0:
            longest_overlap = []
            longest_line = ''
            for line in lines:
                stops = line[0]["Przystanki"]
                overlap = find_matching_subsequence(path_temp, stops)  # Find current overlap using helper function

                # Check for overlaps in reversed line stops
                stops.reverse()
                overlap_reversed = find_matching_subsequence(path_temp, stops)
                stops.reverse()

                # Swap for reversed version if it's longer
                if len(overlap) < len(overlap_reversed):
                    overlap = overlap_reversed

                # Check if current overlap is longer than the previous one, promote trams as they are usually preferred by the people
                if len(overlap) > len(longest_overlap) or (line[0]["Nazwa"] in ['Tramwaj_na_Maslice', 'Tramwaj_na_Swojczyce', 'Tramwaj_Borowska_Szpital', 'Tramwaj_na_Klecine', 'Tramwaj_na_Jagodno', 'Tramwaj_na_Ołtaszyn', 'Tramwaj_na_Gajowice', 'Tramwaj_na_Gądów','Tramwaj_na_Psie_Pole'] and len(overlap)==len(longest_overlap)):
                    longest_overlap = overlap
                    longest_line = line[0]["Nazwa"]

            logging.info(f"Current longest_overlap: {longest_overlap} with line: {longest_line}")

            if longest_overlap:
                name = f"{longest_overlap[0]}-{longest_overlap[-1]}"  # Initialize name for dictionary (it can't store lists as key)
                route.append((name, longest_line))  # Add info to dictionary

                # Remove current longest overlap from path
                if len(longest_overlap) > 2:
                    path_temp = path_temp[
                                len(longest_overlap) - 1:]  # Update path_temp correctly, preserving the last element
                else:
                    path_temp = path_temp[1:]  # Update path_temp correctly

                logging.info(f"Updated path_temp: {path_temp}")
            else:
                break

            # Check if path has 1 element, which means we have finished matching lines, thus remove the last element
            if len(path_temp) == 1:
                path_temp.pop()

        logging.info(f"Final route: {route}")

        return route


'''connection = sqlite3.connect("/Users/dominik/Documents/moje/programowanie/Phyton/Jakniedojade/JakNieDojade/mpk.db")
cursor = connection.cursor()

file1 = open("/Users/dominik/Documents/moje/programowanie/Phyton/Jakniedojade/JakNieDojade/Dane/graph.json", "r")
graph = json.load(file1)
s = ShortestPath()
path = s.dijkstra(graph,13,527)[0]
print(path)
path_a = s.a_star(graph, 13, 527)
print(path_a)
file = open("D:\\PyCharm\\PyCharm 2023.2.4\\JakNieDojade\\Dane\\test2.json","r")
lines = json.load(file)
s.match_lines_to_path(path,lines)
print(s.match_lines_to_path(path,lines))'''
'''file = open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graphtest1.json", "r")
graph = json.load(file)
t=graph
s = ShortestPath()

print(s.dijkstra(t, 20, 553))
#print(s.bellman_ford(t,10,939))'''
