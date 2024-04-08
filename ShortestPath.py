t2 = [[0,10,8,0,0,0,0,0,0],
     [10,0,0,14,8,12,0,0,0],
     [8,0,0,15,13,19,0,0,0],
     [0,14,15,0,0,0,10,25,0],
     [0,8,13,0,0,0,20,18,0],
     [0,12,19,0,0,0,15,11,0],
     [0,0,0,20,20,15,0,0,12],
     [0,0,0,25,18,11,0,0,13],
     [0,0,0,0,0,0,12,13,0]]


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
        while unvisited:  # searching process will continue until it checks all the nodes
            neighbors = [i for i in range(len(graph[current])) if (graph[current][i] != 0 and i in unvisited)]
            for node in neighbors: # consider all neighboring nodes
                dist = distances[node]["val"][1]
                new_dist = distances[current]["val"][1] + t2[current][node]  # calculate the distance from the current node to each neighbor
                if dist == 'inf' or new_dist < dist:  # if the new path is shorter, switch
                    distances[node]["val"][1] = new_dist
                    distances[node]["val"][0] = current
            unvisited.remove(current)  # remove current node from unvisited
            valid = [nodes for nodes in distances if nodes["val"][1] != 'inf' and nodes["node"] in unvisited]  # consider all nodes that connect to current node and are not yet visited
            v = [nodes["val"][1] for nodes in distances if nodes["val"][1] != 'inf' and nodes["node"] in unvisited]  # take their path distances
            for nodes in valid:  # from path distances select the one with the shortest distance
                if nodes["val"][1] == min(v):
                    current = nodes["node"]
        path = reconstruct(distances, start, end)
        length=distances[end]["val"][1]
        return distances, path, length


s = ShortestPath()

print(s.dijkstra(t2, 0, 4))
