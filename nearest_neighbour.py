from Algorithms.ShortestPath import ShortestPath
import json
from Database.FindProject import find_project_root


def graph_creation(graph, start, to_visit) -> tuple:
    stops = [start] + to_visit
    new_graph = [[0]*len(stops) for _ in range(len(stops))]
    indexes = []
    paths = [[0]*len(stops) for _ in range(len(stops))]
    for i in range(len(stops)):
        indexes.append([i, stops[i]])  # Each sublist contains [current_index, IdP]
        for j in range(len(stops)):
            result = s.dijkstra(graph, stops[i], stops[j])
            paths[i][j] = result[0]
            new_graph[i][j] = result[1]
    return new_graph, indexes, paths

def nearest_neighbour(graph, start, to_visit) -> tuple:
    visited = [start]
    tour = [start]
    current = start
    cost = 0
    while len(tour) < len(graph):
        min = float("inf")
        for i in range(len(graph[current])):
            if i not in visited:
                if graph[current][i] < min:
                    min = graph[current][i]
                    next = i
        tour.append(next)
        visited.append(next)
        cost +=graph[current][next]
        current = next
    tour.append(start)
    return tour, cost




project = find_project_root()
file1 = open(project /"Dane/graph.json", "r")
t1 = json.load(file1)

s = ShortestPath

result = graph_creation(t1, 315, [127, 284, 323])
new_graph = result[0]
indexes = result[1]
ultimate_paths = result[2]
# print(indexes)
# print(ultimate_paths)
print(new_graph)

result2 = nearest_neighbour(new_graph, 0, [1,2,3])
print(result2)