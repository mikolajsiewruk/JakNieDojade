import json
import sqlite3
import random
from Algorithms.ShortestPath import ShortestPath
from Visualizations.Visualization import Visualizer
from Simulation.Results import Results


# import a graph with current stops
file = open('D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graph.json','r')
current_graph = json.load(file)

# import a graph with projected changes in public transportation infrastructure
file = open('D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\new_graph.json','r')
new_graph = json.load(file)

# import new public transportation lines
file = open('D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\nowe_linie.json','r',encoding='UTF-8')
lines_file = json.load(file)
new_lines = []
for lines in lines_file:
    new_lines.append(lines[0]["Nazwa"])

# initialize pathfinding modules
sp = ShortestPath()
vis = Visualizer()

# initialize DB connection
db = sqlite3.connect('D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\mpk.db')
cursor = db.cursor()

# create probability list from percentages in database
current_stops_info = cursor.execute("SELECT IdP,Nazwa,Percentage FROM Przystanki_percentages").fetchall()
new_stops_info = cursor.execute("SELECT IdP,Nazwa,Percentage FROM Nowe_przystanki_percentages").fetchall()

stop_ids = []
weights = []

for stop in new_stops_info:
    weights.append(stop[2])
    stop_ids.append(stop[0])

# initialize time counters
current_times = Results()
new_times = Results()

# start Monte Carlo simulation
for i in range(1000):
    start,end = random.choices(stop_ids,weights,k=2)

    path_cur = sp.dijkstra(current_graph,start,end)
    path_new = sp.dijkstra(new_graph,start,end)

print(sp.dijkstra(current_graph,479,272))
print(sp.dijkstra(new_graph,479,272))




