from Algorithms.MinimumSpanningTree import MinimumSpanningTree
from Visualizations.Visualization import Visualizer
from Database.FindProject import find_project_root
import json
import collections
import logging
import time as tm
import random
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt

# logger configuration
logging.basicConfig(
    filename="timing_tsp.log",
    level=logging.INFO,
    format='%(asctime)s [%(processName)s] %(message)s'
)
logger = logging.getLogger(__name__)
project = find_project_root()
vis = Visualizer()

def execute_algorithms(args):
    nodes = args
    with open(project /"Dane/graph.json", "r") as file:  # load a graph
        graph = json.load(file)
    mst = MinimumSpanningTree()
    logging.info(f"Calculating mst through {nodes}")

    start_time = tm.perf_counter_ns()
    kruskal_edges = mst.Kruskal(graph, nodes)
    kruskal_time = tm.perf_counter_ns() - start_time

    start_time = tm.perf_counter_ns()
    prim_edges = mst.Prim(graph, nodes)
    prim_time = tm.perf_counter_ns() - start_time

    return kruskal_time, prim_time, kruskal_edges, prim_edges


def multitask():
    with open(project / "Dane/graph.json", "r") as file:
        graph = json.load(file)

    tasks5 = [[random.randint(1, len(graph)-1) for _ in range(5)] for _ in range(1)]
    tasks10 = [[random.randint(1, len(graph)-1) for _ in range(10)] for _ in range(1)]
    tasks15 = [[random.randint(1, len(graph)-1) for _ in range(15)] for _ in range(1)]
    tasks20 = [[random.randint(1, len(graph)-1) for _ in range(20)] for _ in range(1)]

    with multiprocessing.Pool(8) as pool:
        results5 = pool.map(execute_algorithms, tasks5)
        results10 = pool.map(execute_algorithms, tasks10)
        results15 = pool.map(execute_algorithms, tasks15)
        results20 = pool.map(execute_algorithms, tasks20)

    kruskal_time5 = [result[0] for result in results5]
    kruskal_time10 = [result[0] for result in results10]
    kruskal_time15 = [result[0] for result in results15]
    kruskal_time20 = [result[0] for result in results20]

    prim_time5 = [result[1] for result in results5]
    prim_time10 = [result[1] for result in results10]
    prim_time15 = [result[1] for result in results15]
    prim_time20 = [result[1] for result in results20]

    kruskal_mean5 = np.mean(kruskal_time5)
    kruskal_mean10 = np.mean(kruskal_time10)
    kruskal_mean15 = np.mean(kruskal_time15)
    kruskal_mean20 = np.mean(kruskal_time20)

    prim_mean5 = np.mean(prim_time5)
    prim_mean10 = np.mean(prim_time10)
    prim_mean15 = np.mean(prim_time15)
    prim_mean20 = np.mean(prim_time20)

    kruskal_execution_mean = [kruskal_mean5, kruskal_mean10, kruskal_mean15, kruskal_mean20]
    prim_execution_mean = [prim_mean5, prim_mean10, prim_mean15, prim_mean20]

    plt.plot([5, 10, 15, 20], kruskal_execution_mean, label="Kruskal")
    plt.plot([5, 10, 15, 20], prim_execution_mean, label="Prim")
    plt.title("Kruskal and Prim's Algorithms time consumption comparison")
    plt.xlabel("Number of vertices")
    plt.ylabel("Execution time (ns)")
    plt.legend()
    plt.show()


def path_creation(edges):
    graph = collections.defaultdict(list)
    for edge in edges:
        u = edge[0]
        v = edge[-1]
        graph[u].append((v, tuple(edge)))
        graph[v].append((u, tuple(edge[::-1])))

    def dfs(current, visited_edges, path):
        while graph[current]:
            neighbor, edge = graph[current].pop()
            if edge not in visited_edges:
                visited_edges.add(edge)
                path.extend(list(edge))
                dfs(neighbor, visited_edges, path)

    visited_edges = set()
    start_vertex = edges[0][0]
    full_path = []
    dfs(start_vertex, visited_edges, full_path)

    return full_path

if __name__ == '__main__':
    with open(project / "Dane/graph.json", "r") as file:
        graph = json.load(file)
    results = execute_algorithms([random.randint(1, len(graph)-1) for _ in range(5)])
    kruskal_edges = results[2]
    prim_edges = results[3]
    kruskal_path = path_creation(kruskal_edges)
    prim_path = path_creation(prim_edges)
    vis.draw_graph(graph, "kruskal_map.png", kruskal_path)
    vis.draw_graph(graph, "prim_map.png", prim_path)
    multitask()