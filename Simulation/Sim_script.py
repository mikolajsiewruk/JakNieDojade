import json
import sqlite3
import random
import math
from Algorithms.ShortestPath import ShortestPath
from Visualizations.Visualization import Visualizer
from Simulation.Results import Results
from Database.FindProject import find_project_root

# get project root
project_root = find_project_root()

# import a graph with current stops
file = open(project_root / 'Dane' / 'graph.json','r')
current_graph = json.load(file)

# import a graph with projected changes in public transportation infrastructure
file = open(project_root / 'Dane' / 'new_graph.json','r')
new_graph = json.load(file)

# import all public transportation lines
file = open(project_root / 'Dane' / 'nowe_linie1.json','r',encoding='UTF-8')
all_lines = json.load(file)
all_lines_count = {line[0]["Name"]:0 for line in all_lines}
# import new public transportation lines
file = open(project_root / 'Dane' / 'nowe_linie.json','r',encoding='UTF-8')
lines_file = json.load(file)
new_lines = []
for lines in lines_file:
    new_lines.append(lines[0]["Name"])

# initialize pathfinding modules
sp = ShortestPath()
vis = Visualizer()

# initialize DB connection
db = sqlite3.connect(project_root / 'mpk.db')
cursor = db.cursor()

# create probability list from percentages in database
current_stops_info = cursor.execute("SELECT IdP,Name,Percentage FROM Stops_percentages").fetchall()
new_stops_info = cursor.execute("SELECT IdP,Name,Percentage FROM New_stops_percentages").fetchall()

current_stops_ids = []
stop_ids = []
weights = []
for stop in current_stops_info:
    current_stops_ids.append(stop[0])
for stop in new_stops_info:
    weights.append(stop[2])
    stop_ids.append(stop[0])

# initialize time counters
current_times_stops = Results()
new_times_stops = Results()
current_times_dist = Results()
new_times_dist = Results()

# initialize other counters
total_new_lines_use = 0
total_time_saved = 0
new_paths = 0
new_lines_count = {'Tramwaj_na_Maslice':0,'Tramwaj_na_Swojczyce':0,'Tramwaj_Borowska_Szpital':0,'Tramwaj_na_Klecine':0,'Tramwaj_na_Jagodno':0, 'Tramwaj_na_Ołtaszyn':0, 'Tramwaj_na_Gajowice':0, 'Tramwaj_na_Gądów':0}
total_lines_used = 0
total_time = 0
n = 10
# start Monte Carlo simulation
for i in range(n):
    start,end = random.choices(stop_ids,weights,k=2)

    if start not in current_stops_ids or end not in current_stops_ids:
        new_paths += 1
        path_new, time_new = sp.dijkstra(new_graph, start, end)

        pt_route = sp.match_lines_to_path(path_new, all_lines)
        total_lines_used += len(pt_route)
        for r in pt_route:
            if r[1] in new_lines:
                total_new_lines_use += 1
            all_lines_count[r[1]] += 1
        #vis.draw_graph(new_graph, f"new {i}.png", path_new)
        continue

    path_cur,time_cur = sp.dijkstra(current_graph,start,end)
    path_new,time_new = sp.dijkstra(new_graph,start,end)
    total_time += time_cur

    pt_route = sp.match_lines_to_path(path_new,all_lines)
    total_lines_used += len(pt_route)
    # check if route includes new public transportation lines
    for r in pt_route:
        if r[1] in new_lines:
            total_new_lines_use += 1
            total_time_saved += time_cur - time_new
            # vis.draw_graph(current_graph, f"cur {i}.png", path_cur)
            # vis.draw_graph(new_graph, f"new {i}.png", path_new)

        # count every use of each line
        all_lines_count[r[1]] += 1

    # check distance between stops
    x1,y1 = cursor.execute(f"SELECT X,Y FROM New_stops WHERE IdP = '{start}';").fetchone()
    #print(x1,y1)
    x2,y2 = cursor.execute(f"SELECT X,Y FROM New_stops WHERE IdP = '{end}';").fetchone()
    #print(x2,y2)
    dist = (math.sqrt((pow(x1-x2,2)+pow(y1-y2,2))))*100
    #print(dist)

    # check number of stops in paths
    num_stops_cur = len(path_cur)
    num_stops_new = len(path_new)

    # check the distance between stops
    if dist < 5:
        current_times_dist.under_five.append(time_cur)
        current_times_dist.num_under_five += 1
        new_times_dist.under_five.append(time_new)
        new_times_dist.num_under_five += 1
    elif 5 <= dist < 10:
        current_times_dist.five_ten.append(time_cur)
        current_times_dist.num_five_ten += 1
        new_times_dist.five_ten.append(time_new)
        new_times_dist.num_five_ten += 1
    elif 10 <= dist < 15:
        current_times_dist.ten_fifteen.append(time_cur)
        current_times_dist.num_ten_fifteen += 1
        new_times_dist.ten_fifteen.append(time_new)
        new_times_dist.num_ten_fifteen += 1
    elif 15 <= dist < 20:
        current_times_dist.fifteen_twenty.append(time_cur)
        current_times_dist.num_fifteen_twenty += 1
        new_times_dist.fifteen_twenty.append(time_new)
        new_times_dist.num_fifteen_twenty += 1
    else:
        current_times_dist.over_twenty.append(time_cur)
        current_times_dist.num_over_twenty += 1
        new_times_dist.over_twenty.append(time_new)
        new_times_dist.num_over_twenty += 1

    if num_stops_cur < 5:
        current_times_stops.under_five.append(time_cur)
        current_times_stops.num_under_five += 1
    elif 5 <= num_stops_cur < 10:
        current_times_stops.five_ten.append(time_cur)
        current_times_stops.num_five_ten += 1
    elif 10 <= num_stops_cur < 15:
        current_times_stops.ten_fifteen.append(time_cur)
        current_times_stops.num_ten_fifteen += 1
    elif 15 <= num_stops_cur < 20:
        current_times_stops.fifteen_twenty.append(time_cur)
        current_times_stops.num_fifteen_twenty += 1
    else:
        current_times_stops.over_twenty.append(time_cur)
        current_times_stops.num_over_twenty += 1

    if num_stops_new < 5:
        new_times_stops.under_five.append(time_new)
        new_times_stops.num_under_five += 1
    elif 5 <= num_stops_new < 10:
        new_times_stops.five_ten.append(time_new)
        new_times_stops.num_five_ten += 1
    elif 10 <= num_stops_new < 15:
        new_times_stops.ten_fifteen.append(time_new)
        new_times_stops.num_ten_fifteen += 1
    elif 15 <= num_stops_new < 20:
        new_times_stops.fifteen_twenty.append(time_new)
        new_times_stops.num_fifteen_twenty += 1
    else:
        new_times_stops.over_twenty.append(time_new)
        new_times_stops.num_over_twenty += 1


current_times_stops.draw_boxplot("Current Times by Number of Stops", "current_times_stops.png")
new_times_stops.draw_boxplot("New Times by Number of Stops", "new_times_stops.png")
current_times_dist.draw_boxplot("Current Times by Distance Between Stops", "current_times_dist.png")
new_times_dist.draw_boxplot("New Times by Distance Between Stops", "new_times_dist.png")
print(new_lines_count)
print(total_time_saved)
print(all_lines_count)
print(new_paths)
print(total_new_lines_use)
print(total_lines_used)
print((total_new_lines_use/n)*100)
print(f"mean time saved {(total_time_saved/total_time)*100}")
import pandas as pd
df_all_lines_count = pd.DataFrame(list(all_lines_count.items()), columns=['Line_Name', 'Count'])

# Save the dataframe to a CSV file
df_all_lines_count.to_csv('all_lines_count.csv', index=False)
