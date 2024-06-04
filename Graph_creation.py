import json
from Database.FindProject import find_project_root


table = [[0]*937 for _ in range(937)]
# name of the json file to convert to graph
json_file = 'linie_psie_pole.json'
project_root = find_project_root()
file = open(project_root/ 'Dane' / json_file, 'r')
data = json.load(file)

# name of the graph to be saved
file1 = open(project_root/ 'Dane' / 'graph_psie_pole.json', 'w')

for lines in data:

    stops = lines[0]["Przystanki"]
    times = lines[0]["Czasy"]

    for i in range(len(stops) - 1):
        for j in range(len(stops) - 1):
            if times[j] == 0:
                times[j]=1
            if not table[stops[j]][stops[j + 1]] or table[stops[j]][stops[j + 1]] > times[j]:
                table[stops[j]][stops[j + 1]] = times[j]
                table[stops[j + 1]][stops[j]] = times[j]


json.dump(table, file1, indent=4)
j=0
for i in range(len(table)):
    if sum(table[i]) == 0:
        j+=1
        print(i)
print("total",j)