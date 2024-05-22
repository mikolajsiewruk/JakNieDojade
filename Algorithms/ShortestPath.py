import json
import time as tm

class ShortestPath:

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

    def bellman_ford(self, graph: list,start: int, end: int):
        """
        Finds the shortest path between two stops using the Bellman-Ford algorithm.

        Args:
        - start (int): Index of the starting stop.
        - end (int): Index of the ending stop.

        Returns:
        - tuple: A tuple containing the shortest path from the starting stop to the ending stop and the total travel time.
        """
        num_stops = len(graph)
        # Initialize distances from the starting stop to all other stops as infinity
        distances = [float('inf')] * num_stops
        distances[start] = 0

        # Relaxation loop
        for _ in range(num_stops - 1):
            for current_stop in range(num_stops):
                for next_stop in range(num_stops):
                    if graph[current_stop][next_stop] != 0 and distances[current_stop] != float('inf'):
                        if distances[current_stop] + graph[current_stop][next_stop] < distances[next_stop]:
                            distances[next_stop] = distances[current_stop] + graph[current_stop][next_stop]

        # Check for negative cycles
        '''for current_stop in range(num_stops):
            for next_stop in range(num_stops):
                if graph[current_stop][next_stop] != 0 and distances[current_stop] + graph[current_stop][next_stop] < distances[next_stop]:
                    print("The transportation network contains a negative cycle")
                    return [], float('inf')'''

        # Constructing the path and calculating total travel time
        path = [end]
        current_stop = end
        length = 0
        while current_stop != start:
            for next_stop in range(num_stops):
                if graph[next_stop][current_stop] != 0 and distances[next_stop] == distances[current_stop] - graph[next_stop][current_stop]:
                    path.insert(0, next_stop)
                    length += graph[next_stop][current_stop]
                    current_stop = next_stop
                    break

        return path, length

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
        :returns: returns a list of tuples [(stops,line)]
        """
        def find_matching_subsequence(list1, list2) -> list:
            """
            Helper function for finding a subsequence  starting in the first node of list1
            """
            first_element = list1[0]
            list2 = list(dict.fromkeys(list2))  # remove duplicates from the list cause this caused bugs

            # check if there are no subsequences
            try:
                start_index = list2.index(first_element)
            except ValueError:
                return []

            # Check if list1 is a subsequence starting from this index in list2
            if list2[start_index:start_index + len(list1)] == list1:
                return list2[start_index:start_index + len(list1)]

            longest_subsequence = []
            for i in range(len(list1)):
                # check for longest subsequence if starting index is in line2
                if start_index + i < len(list2) and list1[i] == list2[start_index + i]:
                    longest_subsequence.append(list1[i])
                else:
                    break

            return longest_subsequence

        route = []
        lines_temp = lines.copy()  # copies in case other uses of path and lines are needed
        path_temp = path.copy()

        # loop over path removing stops
        while len(path_temp) > 0:
            longest_overlap = []
            longest_line = ''
            for line in lines_temp:
                stops = line[0]["Przystanki"]
                overlap = find_matching_subsequence(path_temp,stops)  # find current overlap using helper function

                # check for overlaps in reversed line stops
                stops.reverse()
                overlap_reversed = find_matching_subsequence(path_temp,stops)
                stops.reverse()

                # swap for reversed version if it's longer
                if len(overlap) < len(overlap_reversed):
                    overlap = overlap_reversed

                # check if current overlap is longer than previous one
                if len(overlap) > len(longest_overlap):
                    longest_overlap = overlap
                    longest_line = line[0]["Nazwa"]
                    longest_line_dict = line
            print(longest_line_dict)
            print(longest_overlap)
            name = f"{longest_overlap[0]}-{longest_overlap[-1]}"  # initialize name for dictionary (it can't store lists as key)
            route.append((name,longest_line))  # add info to dictionary

            # remove current longest overlap from path, to -1 makes sure the next iteration starts from the right stop
            for elem in longest_overlap[:-1]:
                path_temp.remove(elem)

            # checks if path has 1 element, which means we have finished matching lines, thus removes the last element
            if len(path_temp) == 1:
                path_temp.remove(longest_overlap[-1])

            lines_temp.remove(longest_line_dict)  # remove current longest line from the list to speed up the process

        return route




file1 = open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graph.json", "r")
graph = json.load(file1)
s = ShortestPath()
path = s.dijkstra(graph,257,527)[0]
print(path)
file = open("D:\\PyCharm\\PyCharm 2023.2.4\\JakNieDojade\\Dane\\test2.json","r")
lines = json.load(file)
s.match_lines_to_path(path,lines)
print(s.match_lines_to_path(path,lines))
"""file = open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graphtest1.json", "r")
graph = json.load(file)
t=graph
s = ShortestPath()

print(s.dijkstra(t, 5, 15))
#print(s.bellman_ford(t,10,939))"""