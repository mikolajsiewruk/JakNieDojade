import json
import sqlite3
import random
import math
from Algorithms.ShortestPath import ShortestPath
from Visualizations.Visualization import Visualizer
from Simulation.Results import Results


# import a graph with current stops
file = open('D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graph.json','r')
current_graph = json.load(file)

# import a graph with projected changes in public transportation infrastructure
file = open('D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\new_graph.json','r')
new_graph = json.load(file)

# import all public transportation lines
file = open('D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\nowe_linie1.json','r',encoding='UTF-8')
all_lines = json.load(file)

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

for stop in current_stops_info:
    weights.append(stop[2])
    stop_ids.append(stop[0])

# initialize time counters
current_times_stops = Results()
new_times_stops = Results()
current_times_dist = Results()
new_times_dist = Results()

# start Monte Carlo simulation
for i in range(100):
    start,end = random.choices(stop_ids,weights,k=2)
    print(start,end)
    path_cur,time_cur = sp.dijkstra(current_graph,start,end)
    path_new,time_new = sp.dijkstra(new_graph,start,end)
    pt_route = sp.match_lines_to_path(path_new,all_lines)
    print(path_cur)
    print(path_new)
    print(pt_route)
    # check if route includes new public transportation lines
    for r in pt_route:
        if r[1] in new_lines:
            vis.draw_graph(current_graph, f"cur {i}.png", path_cur)
            vis.draw_graph(new_graph, f"new {i}.png", path_new)

    # check distance between stops
    x1,y1 = cursor.execute(f"SELECT X,Y FROM Nowe_przystanki WHERE IdP = '{start}';").fetchone()
    #print(x1,y1)
    x2,y2 = cursor.execute(f"SELECT X,Y FROM Nowe_przystanki WHERE IdP = '{end}';").fetchone()
    #print(x2,y2)
    dist = (math.sqrt((pow(x1-x2,2)+pow(y1-y2,2))))*100
    #print(dist)

    # check number of stops in paths
    num_stops_cur = len(path_cur)
    num_stops_new = len(path_new)

    # check the distance between stops
    if dist < 5:
        current_times_dist.under_five.append(time_cur)
        new_times_dist.under_five.append(time_new)
    elif 5 <= dist < 10:
        current_times_dist.five_ten.append(time_cur)
        new_times_dist.five_ten.append(time_new)
    elif 10 <= dist < 15:
        current_times_dist.ten_fifteen.append(time_cur)
        new_times_dist.ten_fifteen.append(time_new)
    elif 15 <= dist < 20:
        current_times_dist.fifteen_twenty.append(time_cur)
        new_times_dist.fifteen_twenty.append(time_new)
    else:
        current_times_dist.over_twenty.append(time_cur)
        new_times_dist.over_twenty.append(time_new)

    if num_stops_cur < 5:
        current_times_stops.under_five.append(time_cur)
    elif 5 <= num_stops_cur < 10:
        current_times_stops.five_ten.append(time_cur)
    elif 10 <= num_stops_cur < 15:
        current_times_stops.ten_fifteen.append(time_cur)
    elif 15 <= num_stops_cur < 20:
        current_times_stops.fifteen_twenty.append(time_cur)
    else:
        current_times_stops.over_twenty.append(time_cur)

    if num_stops_new < 5:
        new_times_stops.under_five.append(time_cur)
    elif 5 <= num_stops_new < 10:
        new_times_stops.five_ten.append(time_cur)
    elif 10 <= num_stops_new < 15:
        new_times_stops.ten_fifteen.append(time_cur)
    elif 15 <= num_stops_new < 20:
        new_times_stops.fifteen_twenty.append(time_cur)
    else:
        new_times_stops.over_twenty.append(time_cur)


current_times_stops.draw_boxplot("Current Times by Number of Stops")
new_times_stops.draw_boxplot("New Times by Number of Stops")
current_times_dist.draw_boxplot("Current Times by Distance Between Stops")
new_times_dist.draw_boxplot("New Times by Distance Between Stops")