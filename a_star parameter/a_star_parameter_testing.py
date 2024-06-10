import json
from Database.FindProject import find_project_root
import time as tm
from Algorithms.ShortestPath import ShortestPath
import random as rnd
import matplotlib.pyplot as plt

# code written strictly for tests
# doesn't work anymore
# for it to work one needs to edit the a_star function in ShortestPath.py for it to take the additional parameter
# that would be used to multiply the h_value

# After some testing the value of 300 was chosen to be the most optimal and implemented for good

s = ShortestPath()

project = find_project_root()
file = open(project/"Dane/graph.json", "r")
graf = json.load(file)


times = []
correctness = []

start = int(rnd.randint(1, len(graf) - 1))
end = int(rnd.randint(1, len(graf) - 1))
for i in range(0, 1000,25):
    parameter = i
    results_d = s.dijkstra(graf, start, end)

    timer_start = tm.perf_counter_ns()
    results_a = s.a_star(graf, start, end, parameter)
    timer_end = tm.perf_counter_ns()

    times.append((timer_end - timer_start)/1000000)
    correct = results_a[1]-results_d[1]
    correctness.append(correct)
    if correct == ((timer_end - timer_start)/1000000):
        print(i)


plt.figure()
plt.plot([x for x in range(40)], times, label="Time taken", color="r")
plt.plot([x for x in range(40)], correctness, label="Incorrectness", color="g")
plt.xlabel("Parameter value (iterating with step: 25)")
plt.ylabel("Time")
plt.title("Parameter value and time to do a* search and its incorrectness ")
plt.legend()
plt.show()