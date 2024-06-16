import json
import matplotlib.pyplot as plt
from Algorithms import ShortestPath
from Algorithms import TravellingSalesman
import random
import numpy as np
import multiprocessing
import time as tm
import logging
from Database.FindProject import find_project_root

# logger configuration
logging.basicConfig(
    filename="timing.log",
    level=logging.INFO,
    format='%(asctime)s [%(processName)s] %(message)s'
)
logger = logging.getLogger(__name__)
project = find_project_root()


# function to execute the shortest path search with Dijkstra's, Bellman-Ford and A* algorithm.
def execute_algorithms(args):
    start, end = args
    with open(project /"Dane/graph.json", "r") as file:  # load a graph
        graph = json.load(file)
    sp = ShortestPath.ShortestPath()
    logging.info(f"Calculating paths from {start} to {end}")

    start_time = tm.perf_counter_ns()
    travel_time_dijkstra = sp.dijkstra(graph, start, end)[1]
    dijkstra_time = tm.perf_counter_ns() - start_time

    start_time = tm.perf_counter_ns()
    travel_time_bf = sp.bellman_ford(graph, start, end)[1]
    bellman_ford_time = tm.perf_counter_ns() - start_time

    start_time = tm.perf_counter_ns()
    travel_time_a_star = sp.a_star(graph, start, end)[1]
    a_star_time = tm.perf_counter_ns() - start_time

    return dijkstra_time, bellman_ford_time, a_star_time,travel_time_dijkstra,travel_time_bf,travel_time_a_star

def execute_algorithms_tsp(args):
    start, to_visit = args
    with open(project /"Dane/graph.json", "r") as file:
        graph = json.load(file)
    tsp = TravellingSalesman.TravellingSalesman()
    # logging.info(f"Calculating paths from {start} through {to_visit} back to {start}")

    start_time = tm.perf_counter_ns()
    travel_time_held_karp = tsp.held_karp(graph, start, to_visit)[0]
    held_karp_time = tm.perf_counter_ns() - start_time

    start_time = tm.perf_counter_ns()
    travel_time_nearest_neighbour = tsp.nearest_neighbors(graph, start, to_visit)[0]
    nearest_neighbour_time = tm.perf_counter_ns() - start_time

    return held_karp_time, nearest_neighbour_time, travel_time_held_karp, travel_time_nearest_neighbour


def multitask():
    with open(project /"Dane/graph.json", "r") as file:
        graph = json.load(file)

    tasks = [(random.randint(1, len(graph)-1), random.randint(1, len(graph)-1)) for _ in range(200)]  # generate 500 point pairs for the multiprocesses
    tasks_tsp = [(random.randint(1, len(graph)-1), [random.randint(1, len(graph)-1) for _ in range(5)]) for _ in range(200)]
    with multiprocessing.Pool(16) as pool:
        results = pool.map(execute_algorithms, tasks)
        results_tsp = pool.map(execute_algorithms_tsp, tasks_tsp)

    dijkstra_execution_times = [result[0] for result in results]
    bellman_ford_execution_times = [result[1] for result in results]
    a_star_execution_times = [result[2] for result in results]
    held_karp_execution_times = [result[0] for result in results_tsp]
    nearest_neighbour_execution_times = [result[1] for result in results_tsp]

    dijkstra_execution_mean = np.mean(dijkstra_execution_times)
    bf_execution_mean = np.mean(bellman_ford_execution_times)
    a_star_execution_mean = np.mean(a_star_execution_times)
    held_karp_execution_mean = np.mean(held_karp_execution_times)
    nearest_neighbour_execution_mean = np.mean(nearest_neighbour_execution_times)

    dijkstra_travel_times = [result[3] for result in results]
    bellman_ford_travel_times = [result[4] for result in results]
    a_star_travel_times = [result[5] for result in results]
    held_karp_travel_times = [result[2] for result in results_tsp]
    nearest_neighbour_travel_times = [result[3] for result in results_tsp]

    dijkstra_travel_mean = np.mean(dijkstra_travel_times)
    bf_travel_mean = np.mean(bellman_ford_travel_times)
    a_star_travel_mean = np.mean(a_star_travel_times)
    held_karp_travel_mean = np.mean(held_karp_travel_times)
    nearest_neighbour_travel_mean = np.mean(nearest_neighbour_travel_times)

    labels = ['Dijkstra', 'Bellman-Ford', 'A*']
    avg_execution_times = [dijkstra_execution_mean, bf_execution_mean, a_star_execution_mean]

    plt.bar(labels, avg_execution_times, color=['blue', 'green', 'red'])

    plt.xlabel('Algorithm')
    plt.ylabel('Average Execution Time (ns)')

    plt.title('Comparison of Average Execution Times of Dijkstra, Bellman-Ford and A* Algorithms')
    plt.show()

    labels = ['Dijkstra', 'Bellman-Ford', 'A*']
    avg_travel_times = [dijkstra_travel_mean, bf_travel_mean, a_star_travel_mean]
    plt.bar(labels, avg_travel_times, color=['blue', 'green', 'red'])

    plt.xlabel('Algorithm')
    plt.ylabel('Average Travel time [min]')

    plt.title('Comparison of Average Travel Times of Dijkstra, Bellman-Ford and A* Algorithms')
    plt.show()

    labels = ['Held-karp', 'Nearest Neighbour']
    avg_execution_times = [held_karp_execution_mean, nearest_neighbour_execution_mean]

    plt.bar(labels, avg_execution_times, color=['blue', 'green'])

    plt.xlabel('Algorithm')
    plt.ylabel('Average Execution Time (ns)')

    plt.title('Comparison of Average Execution Times of Held-Karp and Nearest Neighbour Algorithms')
    plt.show()

    avg_travel_times = [held_karp_travel_mean, nearest_neighbour_travel_mean]
    plt.bar(labels, avg_travel_times, color=['blue', 'green'])

    plt.xlabel('Algorithm')
    plt.ylabel('Average Travel time [min]')

    plt.title('Comparison of Average Travel Times of Held-Karp and Nearest Neighbour Algorithms')
    plt.show()

if __name__ == '__main__':
    multitask()