import json
from Algorithms.ShortestPath import ShortestPath
from Database.FindProject import find_project_root


class TravellingSalesman:

    @staticmethod
    def held_karp(graph: list, start: int, to_visit: list) -> tuple:
        """
        Held Karp algorithm for solving the travelling salesman problem
        :param graph: a graph of nodes in adjacency matrix form
        :param start: node to start travelling salesman from
        :param to_visit: nodes to visit in the journey
        :return: a tuple containing the total cost of the journey, the short path and the total path to take
        """

        s = ShortestPath

        def recursion(graph: list, start: int, to_visit: list, reach: int) -> list:
            """
           Held-Karp helper function using recursion to check each time, which node should be the second to last in our path.
           :param graph: a new graph of nodes in adjacency matrix form
           :param start: the node we start the journey from
           :param to_visit: the list of nodes we need to pass in order to reach the reach
           :param reach: ultimately the end of the journey (in the recursion: the current second to last node)
           :return: list featuring total distance of the journey and the path to take
           """
            # if the length of the to_go list is equal to zero we take the value of start-reach directly from the graph
            if len(to_visit) == 0:
                return [graph[reach][start], [start, reach]]
            else:
                min_cost = float('inf')  # setting the min_cost to infinity to make the first cost be always lower than it
                best_path = []
                for stop in to_visit:  # removing one stop at the time from the to_go list
                    new_to_go = to_visit.copy()
                    new_to_go.remove(stop)  # a new list of stops to be visited (to_go) lacks one stop that becomes the reach
                    new_to_reach = stop
                    result = recursion(graph, start, new_to_go, new_to_reach)  # recursion checking all combinations of to_go-reach
                    cost = result[0] + graph[new_to_reach][reach]  # the cost of going from the start to the current second to last stop
                    path = result[1]  # the current path corresponding to the current lowest cost of the journey
                    # updating the best cost and path after each recursion
                    if cost < min_cost:
                        min_cost = cost
                        best_path = path
                return [min_cost, best_path + [reach]]

        stops = [start] + to_visit
        new_graph = [[0] * len(stops) for _ in range(len(stops))]
        indexes = []
        ultimate_paths = [[0] * len(stops) for _ in range(len(stops))]
        for i in range(len(stops)):
            indexes.append([i, stops[i]])  # Each sublist contains [current_index, IdP]
            for j in range(len(stops)):
                result = s.dijkstra(graph, stops[i], stops[j])
                ultimate_paths[i][j] = result[0]  # full paths between nodes in a new graph
                new_graph[i][j] = result[1]  # graph of connections between nodes
        new_to_visit = [index[0] for index in indexes[1:]]

        recursion_results = recursion(new_graph, indexes[0][0], new_to_visit, indexes[0][0])
        cost = recursion_results[0]
        new_path = recursion_results[1]

        reconstruction_results = TravellingSalesman.reconstruction(new_path, indexes, ultimate_paths)
        final_path = reconstruction_results[0]
        final_ultimate_path = reconstruction_results[1]

        return cost, final_path, final_ultimate_path

    @staticmethod
    def nearest_neighbors(graph: list, start: int, to_visit: list) -> tuple:
        """
        Nearest neighbours algorithm for solving the travelling salesman problem
        :param graph: a graph of nodes in adjacency matrix form
        :param start: node to start travelling salesman from
        :param to_visit: nodes to visit in the journey
        :return: a tuple containing the total cost of the journey, the short path and the total path to take
        """

        s = ShortestPath
        stops = [start] + to_visit
        new_graph = [[0] * len(stops) for _ in range(len(stops))]
        indexes = []
        ultimate_paths = [[0] * len(stops) for _ in range(len(stops))]
        for i in range(len(stops)):
            indexes.append([i, stops[i]])  # Each sublist contains [current_index, IdP]
            for j in range(len(stops)):
                result = s.dijkstra(graph, stops[i], stops[j])
                ultimate_paths[i][j] = result[0]  # full paths between nodes in a new graph
                new_graph[i][j] = result[1]  # graph of connections between nodes
        visited = [indexes[0][0]]
        tour = [indexes[0][0]]
        current = indexes[0][0]
        cost = 0
        while len(tour) < len(new_graph):
            min = float("inf")
            for i in range(len(new_graph[current])):
                if i not in visited:
                    if new_graph[current][i] < min:
                        min = new_graph[current][i]
                        next = i
            tour.append(next)
            visited.append(next)
            cost += new_graph[current][next]
            current = next
        tour.append(indexes[0][0])
        cost += new_graph[current][indexes[0][0]]

        reconstruction_results = TravellingSalesman.reconstruction(tour, indexes, ultimate_paths)
        final_path = reconstruction_results[0]
        final_ultimate_path = reconstruction_results[1]

        return cost, final_path, final_ultimate_path

    @staticmethod
    def reconstruction(path: list, indexes: list, ultimate_paths: list) -> tuple:
        """
        Helper function to reconstruct the final path
        :param path: the path from start through nodes to visit to start in a "new" form
        :param indexes: a list  of lists containing the indexes of nodes [in new notation, in old notation]
        :param ultimate_paths: a graph of nodes in adjacency matrix form (containing full paths between them)
        :return: a final path in short and long form
        """
        final_path = []
        final_ultimate_path = []

        for i in range(len(path)):
            start = path[i]
            final_path.append(indexes[start][1])
            try:
                stop = path[i + 1]
                final_ultimate_path.append(ultimate_paths[start][stop])
            except:
                continue

        return final_path, final_ultimate_path


# project_root = find_project_root()
# file = open(project_root/"Dane"/"graph.json", "r")
# graph = json.load(file)
#
# c = TravellingSalesman
# results = c.held_karp(graph, 315, [127, 900, 200])
# print(results[0])
# print(results[1])
# print(results[2])
#
# results2 = c.nearest_neighbors(graph, 315, [127, 900, 200])
# print(results2[0])
# print(results2[1])
# print(results2[2])
# path_new = results2[2]

# path_new_fin = [path_new[0][0]]
# for path in path_new:
#     for n in range(1, len(path)):
#         path_new_fin.append(path[n])
# print(path_new_fin)