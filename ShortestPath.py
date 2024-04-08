t2 = [[0, 2, 0, 5, 0],
      [2, 0, 1, 0, 7],
      [0, 1, 0, 1, 0],
      [5, 0, 1, 0, 4],
      [0, 7, 0, 4, 0]]


class ShortestPath:

    @staticmethod
    def dijkstra(graph: list, start: int, end: int) -> tuple:
        """
        Dijkstra's algorithm for finding the shortest path in a graph.
        :param graph: a graph of nodes in matrix form
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
        while unvisited:
            neighbors = [i for i in range(len(graph[current])) if (graph[current][i] != 0 and i in unvisited)]
            for node in neighbors:
                dist = distances[node]["val"][1]
                new_dist = distances[current]["val"][1] + t2[current][node]
                if dist == 'inf' or new_dist < dist:
                    distances[node]["val"][1] = new_dist
                    distances[node]["val"][0] = current
            unvisited.remove(current)
            valid = [nodes for nodes in distances if nodes["val"][1] != 'inf' and nodes["node"] in unvisited]
            v = [nodes["val"][1] for nodes in distances if nodes["val"][1] != 'inf' and nodes["node"] in unvisited]
            for nodes in valid:
                if nodes["val"][1] == min(v):
                    current = nodes["node"]
        path = reconstruct(distances, start, end)
        return distances, path


s = ShortestPath()

print(s.dijkstra(t2, 0, 4))
