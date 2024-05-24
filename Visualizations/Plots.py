import json
import matplotlib.pyplot as plt
from Algorithms import ShortestPath
import random
import numpy as np
import multiprocessing
import time as tm
import logging

# logger configuration
logging.basicConfig(
    filename="timing.log",
    level=logging.INFO,
    format='%(asctime)s [%(processName)s] %(message)s'
)
logger = logging.getLogger(__name__)

# function to execute the shortest path search with Dijkstra's, Bellman-Ford and A* algorithm.
def execute_algorithms(args):
    start, end = args
    with open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graph.json", "r") as file:  # load a graph
        graph = json.load(file)
    sp = ShortestPath.ShortestPath()
    logging.info(f"Calculating paths from {start} to {end}")

    start_time = tm.perf_counter_ns()
    sp.dijkstra(graph, start, end)
    dijkstra_time = tm.perf_counter_ns() - start_time

    start_time = tm.perf_counter_ns()
    sp.bellman_ford(graph, start, end)
    bellman_ford_time = tm.perf_counter_ns() - start_time

    start_time = tm.perf_counter_ns()
    sp.a_star(graph, start, end)
    a_star_time = tm.perf_counter_ns() - start_time

    return dijkstra_time, bellman_ford_time, a_star_time

def multitask():
    with open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graph.json", "r") as file:
        graph = json.load(file)

    tasks = [(random.randint(1, len(graph)), random.randint(1, len(graph)), random.randint(1, len(graph))) for _ in range(500)]  # generate 500 point pairs for the multiprocesses

    with multiprocessing.Pool(8) as pool:  # initialize 8 processes
        results = pool.map(execute_algorithms, tasks)  # execute 500 tasks using 8 processes

    dijkstra_times = [result[0] for result in results]
    bellman_ford_times = [result[1] for result in results]
    a_star_times = [result[2] for result in results]

    dijkstra_mean = np.mean(dijkstra_times)
    bf_mean = np.mean(bellman_ford_times)
    a_star_mean = np.mean(a_star_times)

    labels = ['Dijkstra', 'Bellman-Ford', 'A*']
    avg_times = [dijkstra_mean, bf_mean, a_star_mean]

    plt.bar(labels, avg_times, color=['blue', 'green', 'red'])

    plt.xlabel('Algorithm')
    plt.ylabel('Average Execution Time (ns)')

    plt.title('Comparison of Average Execution Times of Dijkstra and Bellman-Ford Algorithms')
    plt.show()

if __name__ == '__main__':
    multitask()