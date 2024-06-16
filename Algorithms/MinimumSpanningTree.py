import json
from Algorithms.ShortestPath import ShortestPath
from Database.FindProject import find_project_root

class MinimumSpanningTree:

    @staticmethod
    def Kruskal(graph, nodes):

        s = ShortestPath()

        new_graph = [[0] * len(nodes) for _ in range(len(nodes))]
        ultimate_paths = [[0] * len(nodes) for _ in range(len(nodes))]
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                result = s.dijkstra(graph, nodes[i], nodes[j])
                ultimate_paths[i][j] = result[0]  # full paths between nodes in a new graph
                new_graph[i][j] = result[1]  # graph of connections between nodes

        graph_list = []
        for i in range(len(new_graph)):
            for j in range(i, len(new_graph)):
                if new_graph[i][j] != 0:
                    graph_list.append([i, j, new_graph[i][j]])

        def find(parent, i):
            if parent[i] == i:
                return i
            return find(parent, parent[i])

        def union(parent, rank, x, y):
            x_root = find(parent, x)
            y_root = find(parent, y)
            if rank[x_root] < rank[y_root]:
                parent[x_root] = y_root
            elif rank[x_root] > rank[y_root]:
                parent[y_root] = x_root
            else:
                parent[y_root] = x_root
                rank[x_root] += 1

        result = []
        i, e = 0, 0
        graph_list = sorted(graph_list, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(len(nodes)):
            parent.append(node)
            rank.append(0)
        while e < len(nodes) - 1:
            u, v, weight = graph_list[i]
            i += 1
            x = find(parent, u)
            y = find(parent, v)
            if x != y:
                e +=1
                result.append([u, v, weight])
                union(parent, rank, x, y)
        final_results = MinimumSpanningTree.reconstruction(result, ultimate_paths)

        return final_results

    @staticmethod
    def Prim(graph, nodes):

        s = ShortestPath()

        new_graph = [[0] * len(nodes) for _ in range(len(nodes))]
        ultimate_paths = [[0] * len(nodes) for _ in range(len(nodes))]
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                result = s.dijkstra(graph, nodes[i], nodes[j])
                ultimate_paths[i][j] = result[0]  # full paths between nodes in a new graph
                new_graph[i][j] = result[1]  # graph of connections between nodes

        v_in_mst = set()
        v_not_in_mst = set((x for x in range(len(new_graph))))
        start = list(v_not_in_mst)[0]
        v_in_mst.add(start)
        v_not_in_mst.remove(start)
        edges = []
        while len(v_in_mst) < len(nodes):
            min = float('inf')
            for node_in_mst in v_in_mst:
                for node_not_in_mst in v_not_in_mst:
                    if new_graph[node_in_mst][node_not_in_mst] < min:
                        min = new_graph[node_in_mst][node_not_in_mst]
                        vertex = node_in_mst
                        closest = node_not_in_mst
            edges.append([vertex, closest])
            v_in_mst.add(closest)
            v_not_in_mst.remove(closest)

        final_results = MinimumSpanningTree.reconstruction(edges, ultimate_paths)

        return final_results


    @staticmethod
    def reconstruction(edges, ultimate_paths):

        actual_edges = []
        for i in range(len(edges)):
            start = edges[i][0]
            stop = edges[i][1]
            actual_edges.append(ultimate_paths[start][stop])
        return actual_edges

# project = find_project_root()
# file = open(project/"Dane"/"graph.json", "r")
# graph = json.load(file)
#
# m = MinimumSpanningTree
# result = m.Kruskal(graph, [37, 84, 52, 901, 720, 605])
# print(result)
# result2 = m.Prim(graph, [37, 84, 52, 901, 720, 605])
# print(result2)
