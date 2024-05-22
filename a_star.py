import sqlite3
import numpy as np
import json


def f_value(node, x_goal, y_goal):
    g_value = node[2]
    h_value = np.sqrt((node[3]-x_goal)**2 + (node[4]-y_goal)**2)
    f_value = g_value + h_value
    return f_value

def reconstruct_path(closed_list, current):
    route = []
    value = current[2]
    while current is not None:
        route.append(current[1])
        parent = current[0]
        current = next((node for node in closed_list if node[1] == parent), None)
    return route[::-1], value

def a_star(start, goal):
    open_list = []
    x_start = cursor.execute(f"select X from Przystanki where IdP = '{start}';").fetchone()[0]
    y_start = cursor.execute(f"select Y from Przystanki where IdP = '{start}';").fetchone()[0]
    open_list.append([None, start, 0, x_start, y_start]) # parent, node and node's g value, x coordinate, y coordinate
    closed_list = []
    x_goal = cursor.execute(f"select X from Przystanki where IdP = '{goal}';").fetchone()[0]
    y_goal = cursor.execute(f"select Y from Przystanki where IdP = '{goal}';").fetchone()[0]
    current = None
    while open_list:
        lowest_f = f_value(open_list[0], x_goal, y_goal)
        current = open_list[0]
        for node in open_list:
            if f_value(node, x_goal, y_goal) < lowest_f:
                lowest_f = f_value(node, x_goal, y_goal)
                current = node
        if current[1] == goal:
            closed_list.append(current)
            return reconstruct_path(closed_list, current)
        open_list.remove(current)
        closed_list.append(current)
        for i in range(len(graph[0])):
            if graph[current[1]][i] == 0 or any(element[1] == i for element in closed_list):
                continue
            else:
                if any(element[1] == i for element in open_list):
                    neigbour_g = current[2] + graph[current[1]][i]
                    for j in range(len(open_list)):
                        if open_list[j][1] == i:
                            if open_list[j][2] > neigbour_g:
                                x = cursor.execute(f"select X from Przystanki where IdP = '{j}';").fetchone()[0]
                                y = cursor.execute(f"select Y from Przystanki where IdP = '{j}';").fetchone()[0]
                                open_list[j] = [current[1], j, neigbour_g, x, y]
                else:
                    neigbour_g = current[2] + graph[current[1]][i]
                    x = cursor.execute(f"select X from Przystanki where IdP = '{i}';").fetchone()[0]
                    y = cursor.execute(f"select Y from Przystanki where IdP = '{i}';").fetchone()[0]
                    open_list.append([current[1], i, neigbour_g, x, y])

    return False


connection = sqlite3.connect("mpk.db")
cursor = connection.cursor()

file = open("/Users/dominik/Documents/moje/programowanie/Phyton/Jakniedojade/JakNieDojade/Dane/graph.json", "r")
graph = json.load(file)

path = a_star(1, 815)
print(path)

