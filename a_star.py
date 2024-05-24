import sqlite3
import numpy as np
import json




def a_star(graph: list, start: int, goal: int) -> tuple:
    """
    A* heuristic algorithm for finding the shortest path in a graph.
    :param graph: a graph of nodes in adjacency matrix form
    :param start: start node
    :param goal: goal node
    :return: tuple
    """

    def f_value(node: list) -> float:
        """
        A* Helper function, determining the f_value of the given node.
        :param node: node which f_value will be calculated
        :return: f_value of the given node
        """
        g_value = node[2]
        h_value = np.sqrt((node[3] - x_goal) ** 2 + (node[4] - y_goal) ** 2)
        f_value = g_value + h_value
        print(f_value)
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
    x_start = cursor.execute(f"select X from Przystanki where IdP = '{start}';").fetchone()[0]
    y_start = cursor.execute(f"select Y from Przystanki where IdP = '{start}';").fetchone()[0]
    # THE WAY NODES IN OPEN AND CLOSED LISTS ARE STORED: [node's parent, node and node's g value, x coordinate, y coordinate]
    open_list.append([None, start, 0, x_start, y_start])
    x_goal = cursor.execute(f"select X from Przystanki where IdP = '{goal}';").fetchone()[0]
    y_goal = cursor.execute(f"select Y from Przystanki where IdP = '{goal}';").fetchone()[0]

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
                                x = cursor.execute(f"select X from Przystanki where IdP = '{j}';").fetchone()[0]
                                y = cursor.execute(f"select Y from Przystanki where IdP = '{j}';").fetchone()[0]
                                open_list[j] = [current[1], i, neighbour_g, x, y]

                # if the neighbour is not in the open list, add it to open list
                else:
                    neighbour_g = current[2] + graph[current[1]][i]
                    x = cursor.execute(f"select X from Przystanki where IdP = '{i}';").fetchone()[0]
                    y = cursor.execute(f"select Y from Przystanki where IdP = '{i}';").fetchone()[0]
                    open_list.append([current[1], i, neighbour_g, x, y])

    # if the open list is empty and path has not been determined: no path possible, return false
    return False


connection = sqlite3.connect("mpk.db")
cursor = connection.cursor()

file = open("/Users/dominik/Documents/moje/programowanie/Phyton/Jakniedojade/JakNieDojade/Dane/graph.json", "r")
graf = json.load(file)

path = a_star(graf, 257, 527)
print(path)

