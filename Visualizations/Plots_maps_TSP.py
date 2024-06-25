
import json
import time as tm
import multiprocessing
import random
import matplotlib.pyplot as plt
import numpy as np
import logging
from Database.FindProject import find_project_root
from Algorithms.TravellingSalesman import TravellingSalesman
from Visualizations.Visualization import Visualizer

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
    start, to_visit = args
    with open(project /"Dane/graph.json", "r") as file:  # load a graph
        graph = json.load(file)
    tsp = TravellingSalesman()
    logging.info(f"Calculating paths from {start} through {to_visit}")

    start_time = tm.perf_counter_ns()
    held_karp_path = tsp.held_karp(graph, start, to_visit)[2]
    held_karp_time = tm.perf_counter_ns() - start_time

    start_time = tm.perf_counter_ns()
    nearest_neighbour_path = tsp.nearest_neighbors(graph, start, to_visit)[2]
    nearest_neighbour_time = tm.perf_counter_ns() - start_time

    return held_karp_time, nearest_neighbour_time, held_karp_path, nearest_neighbour_path

def multitask():
    with open(project / "Dane/graph.json", "r") as file:
        graph = json.load(file)

    tasks5 = [(random.randint(1, len(graph)-1), [random.randint(1, len(graph)-1) for _ in range(4)]) for _ in range(200)]
    tasks10 = [(random.randint(1, len(graph)-1), [random.randint(1, len(graph)-1) for _ in range(6)]) for _ in range(200)]
    tasks15 = [(random.randint(1, len(graph)-1), [random.randint(1, len(graph)-1) for _ in range(8)]) for _ in range(200)]
    tasks20 = [(random.randint(1, len(graph)-1), [random.randint(1, len(graph)-1) for _ in range(10)]) for _ in range(200)]

    with multiprocessing.Pool(8) as pool:
        results5 = pool.map(execute_algorithms, tasks5)
        results10 = pool.map(execute_algorithms, tasks10)
        results15 = pool.map(execute_algorithms, tasks15)
        results20 = pool.map(execute_algorithms, tasks20)

    held_karp_time5 = [result[0] for result in results5]
    held_karp_time10 = [result[0] for result in results10]
    held_karp_time15 = [result[0] for result in results15]
    held_karp_time20 = [result[0] for result in results20]

    nearest_neighbour5 = [result[1] for result in results5]
    nearest_neighbour10 = [result[1] for result in results10]
    nearest_neighbour15 = [result[1] for result in results15]
    nearest_neighbour20 = [result[1] for result in results20]

    held_karp_mean5 = np.mean(held_karp_time5)
    held_karp_mean10 = np.mean(held_karp_time10)
    held_karp_mean15 = np.mean(held_karp_time15)
    held_karp_mean20 = np.mean(held_karp_time20)

    nearest_neighbour_mean5 = np.mean(nearest_neighbour5)
    nearest_neighbour_mean10 = np.mean(nearest_neighbour10)
    nearest_neighbour_mean15 = np.mean(nearest_neighbour15)
    nearest_neighbour_mean20 = np.mean(nearest_neighbour20)

    held_karp_execution_mean = [held_karp_mean5, held_karp_mean10, held_karp_mean15, held_karp_mean20]
    nearest_neighbour_execution_mean = [nearest_neighbour_mean5, nearest_neighbour_mean10, nearest_neighbour_mean15, nearest_neighbour_mean20]

    plt.plot([4,6,8,10], held_karp_execution_mean, label="Held-Karp")
    plt.plot([4,6,8,10], nearest_neighbour_execution_mean, label="Nearest Neighbour")
    plt.title("Held-Karp and Nearest Neighbour Algorithms time consumption comparison")
    plt.xlabel("Number of vertices")
    plt.ylabel("Execution time (ns)")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    with open(project / "Dane/graph.json", "r") as file:
        graph = json.load(file)
    results = execute_algorithms([random.randint(1, len(graph)-1), [random.randint(1, len(graph)-1) for _ in range(5)]])
    held_karp_path = results[2]
    nearest_neighbour_path = results[3]
    held_karp_path_final = []
    nearest_neighbour_path_final = []
    for i in range(len(held_karp_path)):
        for j in range(len(held_karp_path[i])-1):
            held_karp_path_final.append(held_karp_path[i][j])
        for j in range(len(nearest_neighbour_path[i])-1):
            nearest_neighbour_path_final.append(nearest_neighbour_path[i][j])
    held_karp_path_final.append(held_karp_path[0][0])
    nearest_neighbour_path_final.append(nearest_neighbour_path[0][0])
    vis.draw_graph(graph, "held_karp_map.png", held_karp_path_final)
    vis.draw_graph(graph, "nearest_neighbour_map.png", nearest_neighbour_path_final)
    multitask()
