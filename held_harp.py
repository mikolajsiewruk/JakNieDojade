from Algorithms.ShortestPath import ShortestPath
import json


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


def held_karp(graph: list, start: int, to_go: list, reach: int) -> list:
    """
           Held Karp algorithm for solving the travelling salesman problem
           using recursion to check each time, which node should be the second to last in our path.
           :param graph: a graph of nodes in adjacency matrix form
           :param start: the node we start the journey from
           :param to_go: the list of nodes we need to pass in order to reach the reach
           :param reach: ultimately the end of the journey (in the recursion: the current second to last node)
           :return: list featuring total distance of the journey and the path to take
           """
    # if the lenght of the to_go list is equal to zero we take the value of start-reach directly from the graph
    if len(to_go) == 0:
        return [graph[reach][start], [start, reach]]
    else:
        min_cost = float('inf')  # setting the min_cost to infinity to make the first cost be always lower than it
        best_path = []
        for stop in to_go:  # removing one stop at the time from the to_go list
            new_to_go = to_go.copy()
            new_to_go.remove(stop)  # a new list of stops to be visited (to_go) lacks one stop that becomes the reach
            new_to_reach = stop
            result = held_karp(graph, start, new_to_go, new_to_reach)  # recursion checking all combinations of to_go-reach
            cost = result[0] + graph[new_to_reach][reach]  # the cost of going from the start to the current second to last stop
            path = result[1]  # the current path corresponding to the current lowest cost of the journey
            # updating the best cost and path after each recursion
            # print("Droga ", path)
            if cost < min_cost:
                min_cost = cost
                best_path = path
            # print("Aktualne", to_go)
            # print("Koszt", min_cost)
            #     print("Najlepsza droga ", best_path)
        return [min_cost, best_path + [reach]]

# krótki opis jak to ma działać
# zaczynamy w 0
# szukamy C({1,2,3}, 0)
# nie wiemy jaka jest min(C({1,2},3)+graph[3][0], C({1,3}, 2)+graph[2][0], C({2,3},1)+graph[1][0])
# ale teraz nie wiemy jaka jest min(C({1},2)+graph[2][3], C({2},1)+graph[1][3]) ... tak samo dla pozostałych przypadków
# a potem nie wiemy jaka jest min(C{},1)+graph[1][2]
# i to już można policzyć, bo to jest graph[0][1]

def reconstrucion(path, indexes, ultimate_paths):
    final_path = []
    big_path = []

    for i in range(len(path)):
        start = path[i]
        final_path.append(indexes[start][1])
        try:
            stop = path[i+1]
            big_path.append(ultimate_paths[start][stop])
        except:
            continue

    return final_path, big_path


file1 = open("/Users/dominik/Documents/moje/programowanie/Phyton/Jakniedojade/JakNieDojade/Dane/graph.json", "r")
t1 = json.load(file1)

s = ShortestPath

result = graph_creation(t1, 315, [127, 284, 315])
new_graph = result[0]
indexes = result[1]
ultimate_paths = result[2]
# print(indexes)
print(ultimate_paths)

result2 = held_karp(new_graph, 0, [1,2,3], 0)
cost = result2[0]
new_path = result2[1]
print(cost)
print(new_path)

result3 = reconstrucion(new_path, indexes, ultimate_paths)
final_path = result3[0]
big_path = result3[1]
print(final_path)
print(big_path)
