import json
import sqlite3
import random
import math
import numpy as np
import pandas as pd
from Algorithms.TravellingSalesman import TravellingSalesman
from Algorithms.ShortestPath import ShortestPath
from Visualizations.Visualization import Visualizer
from Simulation.Results_tsp import Results_tsp
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
tsp = TravellingSalesman()
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
current_times_stops = Results_tsp()
new_times_stops = Results_tsp()
current_times_dist = Results_tsp()
new_times_dist = Results_tsp()

# initialize other counters
total_new_lines_use = 0
total_time_saved = 0
new_paths = 0
new_lines_count = {'Tramwaj_na_Maslice':0,'Tramwaj_na_Swojczyce':0,'Tramwaj_Borowska_Szpital':0,'Tramwaj_na_Klecine':0,'Tramwaj_na_Jagodno':0, 'Tramwaj_na_Ołtaszyn':0, 'Tramwaj_na_Gajowice':0, 'Tramwaj_na_Gądów':0}

# start Monte Carlo simulation
for i in range(20):
    start = random.choices(stop_ids,weights)
    to_visit = [random.choices(stop_ids, weights)[0] for _ in range(5)]

    if start[0] not in current_stops_ids or any(item not in current_stops_ids for item in to_visit):
        new_paths += 1
        time_new, x, path_new = tsp.nearest_neighbors(new_graph, start[0], to_visit)

        path_new_fin = [path_new[0][0]]
        for path in path_new:
            for n in range(1, len(path)):
                path_new_fin.append(path[n])

        pt_route = sp.match_lines_to_path(path_new_fin, all_lines)

        for r in pt_route:
            if r[1] in new_lines:
                total_new_lines_use += 1
            all_lines_count[r[1]] += 1
        vis.draw_graph(new_graph, f"new {i}.png", path_new_fin)
        continue

    time_cur, _, path_cur = tsp.nearest_neighbors(current_graph, start[0], to_visit)
    time_new, _, path_new = tsp.nearest_neighbors(new_graph, start[0], to_visit)
    path_cur_fin = [path_cur[0][0]]
    for path in path_cur:
        for n in range(1, len(path)):
            path_cur_fin.append(path[n])

    path_new_fin = [path_new[0][0]]
    for path in path_new:
        for n in range(1, len(path)):
            path_new_fin.append(path[n])

    pt_route = sp.match_lines_to_path(path_new_fin, all_lines)

    # check if route includes new public transportation lines
    for r in pt_route:
        if r[1] in new_lines:
            total_new_lines_use += 1
            total_time_saved += time_cur - time_new
            vis.draw_graph(current_graph, f"cur {i}.png", path_cur_fin)
            vis.draw_graph(new_graph, f"new {i}.png", path_new_fin)

        # count every use of each line
        all_lines_count[r[1]] += 1

    all_stops = start + to_visit
    counter = 0
    distances = []
    while len(distances) < int(((math.factorial(len(all_stops))/(2*(math.factorial(len(all_stops)-2)))))):
        for k in range(counter+1, len(all_stops)):
            # check distance between stops
            x1,y1 = cursor.execute(f"SELECT X,Y FROM New_stops WHERE IdP = '{all_stops[counter]}';").fetchone()
            #print(x1,y1)
            x2,y2 = cursor.execute(f"SELECT X,Y FROM New_stops WHERE IdP = '{all_stops[k]}';").fetchone()
            #print(x2,y2)
            dist = (math.sqrt((pow(x1-x2,2)+pow(y1-y2,2))))*100
            #print(dist)
            distances.append(dist)
        counter +=1

    dist_mean = np.mean(distances)

    # check number of stops in paths
    num_stops_cur = len(path_cur_fin)
    num_stops_new = len(path_new_fin)

    # check the distance between stops
    if dist_mean < 10:
        current_times_dist.under_ten.append(time_cur)
        current_times_dist.num_under_ten += 1
        new_times_dist.under_ten.append(time_new)
        new_times_dist.num_under_ten += 1
    elif 10 <= dist_mean < 13:
        current_times_dist.ten_thirteen.append(time_cur)
        current_times_dist.num_ten_thirteen += 1
        new_times_dist.ten_thirteen.append(time_new)
        new_times_dist.num_ten_thirteen += 1
    elif 13 <= dist_mean < 16:
        current_times_dist.thirteen_sixteen.append(time_cur)
        current_times_dist.num_thirteen_sixteen += 1
        new_times_dist.thirteen_sixteen.append(time_new)
        new_times_dist.num_thirteen_sixteen += 1
    elif 16 <= dist_mean < 19:
        current_times_dist.sixteen_nineteen.append(time_cur)
        current_times_dist.num_sixteen_nineteen += 1
        new_times_dist.sixteen_nineteen.append(time_new)
        new_times_dist.num_sixteen_nineteen += 1
    else:
        current_times_dist.over_nineteen.append(time_cur)
        current_times_dist.num_over_nineteen += 1
        new_times_dist.over_nineteen.append(time_new)
        new_times_dist.num_over_nineteen += 1


    if num_stops_cur < 90:
        current_times_stops.under_ninety.append(time_cur)
        current_times_stops.num_under_ninety += 1
    elif 90 <= num_stops_cur < 100:
        current_times_stops.ninety_hundred.append(time_cur)
        current_times_stops.num_ninety_hundred += 1
    elif 100 <= num_stops_cur < 110:
        current_times_stops.hundred_hundredten.append(time_cur)
        current_times_stops.num_hundred_hundredten += 1
    elif 110 <= num_stops_cur < 120:
        current_times_stops.hundredten_hundredtwenty.append(time_cur)
        current_times_stops.num_hundredten_hundredtwenty += 1
    else:
        current_times_stops.over_hundredtwenty.append(time_cur)
        current_times_stops.num_over_hundredtwenty += 1

    if num_stops_new < 90:
        new_times_stops.under_ninety.append(time_new)
        new_times_stops.num_under_ninety += 1
    elif 90 <= num_stops_new < 100:
        new_times_stops.ninety_hundred.append(time_new)
        new_times_stops.num_ninety_hundred += 1
    elif 100 <= num_stops_new < 110:
        new_times_stops.hundred_hundredten.append(time_new)
        new_times_stops.num_hundred_hundredten += 1
    elif 110 <= num_stops_new < 120:
        new_times_stops.hundredten_hundredtwenty.append(time_new)
        new_times_stops.num_hundredten_hundredtwenty += 1
    else:
        new_times_stops.over_hundredtwenty.append(time_new)
        new_times_stops.num_over_hundredtwenty += 1


current_times_stops.draw_boxplot("Current Times by Number of Stops", "current_times_stops.png", 1)
new_times_stops.draw_boxplot("New Times by Number of Stops", "new_times_stops.png", 1)
current_times_dist.draw_boxplot("Current Times by Distance Between Stops", "current_times_dist.png", 0)
new_times_dist.draw_boxplot("New Times by Distance Between Stops", "new_times_dist.png", 0)
print(new_lines_count)
print(total_time_saved)
print(all_lines_count)

d = all_lines_count
df = pd.DataFrame(list(d.items()), columns=['Line', 'Quantity'])
csv_file_path = project_root / 'Simulation' / 'lines_quantity_tsp.csv'
df.to_csv(csv_file_path, index=False)
