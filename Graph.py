import json
f=open("Dane/lines.json", "r")

data = json.load(f)
line1={
            "Nazwa": "Materials\\Linia_1.txt",
            "Przystanki": [
                539,
                831,
                392,
                294,
                70,
                776,
                121,
                121,
                760,
                489,
                848,
                596,
                569,
                532,
                324,
                213,
                854,
                772,
                108,
                578,
                711,
                939
            ],
            "Czasy": [
                1,
                1,
                1,
                2,
                3,
                2,
                1,
                2,
                2,
                2,
                1,
                2,
                3,
                2,
                2,
                1,
                1,
                2,
                1,
                1,
                2
            ]
        }
table=[]
for i in range (0,940):
    a=[]
    for j in range (0,940):
        a.append(0)
    table.append(a)
for di in data:
    print(di)

    stops=di[0]["Przystanki"]
    times=di[0]["Czasy"]

    for i in range(len(stops)-1):
        if not table[stops[i]][stops[i+1]]:
            table[stops[i]][stops[i+1]]=times[i]
            table[stops[i+1]][stops[i]]= times[i]

print(table)
