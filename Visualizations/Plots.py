import json
import matplotlib.pyplot as plt
from Algorithms import ShortestPath
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

def multitask():
    with open(project /"Dane/graph.json", "r") as file:
        graph = json.load(file)

    tasks = [(random.randint(1, len(graph)-1), random.randint(1, len(graph)-1)) for _ in range(200)]  # generate 500 point pairs for the multiprocesses

    with multiprocessing.Pool(16) as pool:
        results = pool.map(execute_algorithms, tasks)

    dijkstra_execution_times = [result[0] for result in results]
    bellman_ford_execution_times = [result[1] for result in results]
    a_star_execution_times = [result[2] for result in results]

    dijkstra_execution_mean = np.mean(dijkstra_execution_times)
    bf_execution_mean = np.mean(bellman_ford_execution_times)
    a_star_execution_mean = np.mean(a_star_execution_times)

    dijkstra_travel_times = [result[3] for result in results]
    bellman_ford_travel_times = [result[4] for result in results]
    a_star_travel_times = [result[5] for result in results]

    dijkstra_travel_mean = np.mean(dijkstra_travel_times)
    bf_travel_mean = np.mean(bellman_ford_travel_times)
    a_star_travel_mean = np.mean(a_star_travel_times)

    labels = ['Dijkstra', 'Bellman-Ford', 'A*']
    avg_execution_times = [dijkstra_execution_mean, bf_execution_mean, a_star_execution_mean]

    plt.bar(labels, avg_execution_times, color=['blue', 'green', 'red'])

    plt.xlabel('Algorithm')
    plt.ylabel('Average Execution Time (ns)')

    plt.title('Comparison of Average Execution Times of Dijkstra and Bellman-Ford Algorithms')
    plt.show()

    labels = ['Dijkstra', 'Bellman-Ford', 'A*']
    avg_travel_times = [dijkstra_travel_mean, bf_travel_mean, a_star_travel_mean]
    plt.bar(labels, avg_travel_times, color=['blue', 'green', 'red'])

    plt.xlabel('Algorithm')
    plt.ylabel('Average Travel time [min]')

    plt.title('Comparison of Average Travel Times of Dijkstra and Bellman-Ford Algorithms')
    plt.show()

if __name__ == '__main__':
    multitask()