import json
import sqlite3
import random
import math
import os
from Algorithms.ShortestPath import ShortestPath
from Visualizations.Visualization import Visualizer
from Simulation.Results import Results
from Database.FindProject import find_project_root

# the name of the estate to simulate
area_of_choice = "Gajowice"
graph_name = 'graph_gajowice.json'
line_file_name = 'linie_gajowice.json'

# get project root
project_root = find_project_root()

# import a graph with current stops
file = open(project_root / 'Dane' / 'graph.json', 'r')
current_graph = json.load(file)

# import a graph with projected changes in public transportation infrastructure
file = open(project_root / 'Dane' / graph_name, 'r')
new_graph = json.load(file)

# import current public transportation lines with one projected
file = open(project_root / 'Dane' / line_file_name, 'r', encoding='UTF-8')
all_lines = json.load(file)
all_lines_count = {line[0]["Nazwa"]:0 for line in all_lines}
line_name = all_lines[-1][0].get("Nazwa")

# initialize pathfinding modules
sp = ShortestPath()
vis = Visualizer()

# initialize DB connection
db = sqlite3.connect(project_root / 'mpk.db')
cursor = db.cursor()

# getting start stops
start_stops_info = cursor.execute("SELECT IdP,NAME,Percentage FROM New_stops_percentages WHERE AREA = " + "'" + area_of_choice + "'").fetchall()
start_stops = []
for stops in start_stops_info:
    start_stops.append(stops[0])

# getting weights of directions
file = open(project_root / "% osiedli i celu korzystania z komunikacji.json", "r", encoding='UTF-8')
file1 = json.load(file)
osiedle_directions = []
directions = ["Szkola", "Praca", "Zakupy", "Rozrywka", "Restauracje", "Spotkania", "Zdrowie", "Kultura"] # tu zmienic
direction_weights = []
for osiedle in file1:
    if osiedle[0]["Nazwa"] == area_of_choice:
        for direction in directions:
            direction_weights.append(osiedle[0][direction])

# initialize time counters
current_times_stops = Results()
new_times_stops = Results()
current_times_dist = Results()
new_times_dist = Results()

# initialize other counters
total_new_lines_use = 0
total_time_saved = 0
new_path = 0

# start Monte Carlo simulation
for i in range(2):
    start = random.choice(start_stops)
    if start >= 913:
        new_path += 1
        continue
    random_direction = random.choices(directions, direction_weights)[0]
    end_stops_info = (cursor.execute("SELECT IdP, (SCHOOL + LABOUR + SHOPS + LEISURE + RESTAURANTS + SOCIAL + HEALTH + CULTURE)"
                                       ", Percentage FROM Stops_percentages WHERE "+random_direction+"=1").fetchall())
    end_stops = []
    end_stops_weights = []
    for j in range(len(end_stops_info)):
        end_stops.append(end_stops_info[j][0])
        end_stops_weights.append(end_stops_info[j][1] * 3 + end_stops_info[j][2])  # wzór: suma jedynek * 3 + populacja osiedla

    finish = random.choices(end_stops, end_stops_weights)[0]
    # print(finish)

    path_cur, time_cur = sp.dijkstra(current_graph, start, finish)
    path_new, time_new = sp.dijkstra(new_graph, start, finish)

    pt_route = sp.match_lines_to_path(path_new, all_lines)

    # check if route includes new public transportation lines
    for r in pt_route:
        if r[1] == line_name:
            total_new_lines_use += 1
            total_time_saved += time_cur - time_new
            vis.draw_graph(current_graph, f"cur {i}.png", path_cur)
            vis.draw_graph(new_graph, f"new {i}.png", path_new)

        # count every use of each line
        all_lines_count[r[1]] += 1

    # check distance between stops
    x1, y1 = cursor.execute(f"SELECT X,Y FROM New_stops WHERE IdP = '{start}';").fetchone()
    # print(x1,y1)
    x2, y2 = cursor.execute(f"SELECT X,Y FROM New_stops WHERE IdP = '{finish}';").fetchone()
    # print(x2,y2)
    dist = (math.sqrt((pow(x1 - x2, 2) + pow(y1 - y2, 2)))) * 100
    # print(dist)

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

current_times_stops.draw_boxplot("Current Times by Number of Stops")
new_times_stops.draw_boxplot("New Times by Number of Stops")
current_times_dist.draw_boxplot("Current Times by Distance Between Stops")
new_times_dist.draw_boxplot("New Times by Distance Between Stops")
print(total_time_saved)
print(all_lines_count)
print(new_path)

