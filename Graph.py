import json
'''f=open("Dane/lines.json", "r")

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
'''

# with open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\lines.json","r",encoding="UTF-8") as file:
#     bus1 = json.load(open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\bus1.json",'r'))
#     bus = json.load(open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\bus.json",'r'))
#     a = json.load(file)
#     for items in bus:
#         a.append(items)
#     for i2 in bus1:
#         a.append(i2)
#     json.dump(a,open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\all_lines.json",'w'),indent=4)

table = [[0]*914 for _ in range(914)]
file = open('D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\test2.json','r')
data = json.load(file)

for lines in data:
    print(lines)

    stops = lines[0]["Przystanki"]
    times = lines[0]["Czasy"]

    for i in range(len(stops) - 1):
        print(len(times), i)
        print(stops[i])
        print(stops[i + 1])
        print(len(stops),len(times))
        for i in range(len(stops) - 1):
            if times[i] == 0:
                times[i]=1
            if not table[stops[i]][stops[i + 1]] or table[stops[i]][stops[i + 1]] > times[i]:
                table[stops[i]][stops[i + 1]] = times[i]
                table[stops[i + 1]][stops[i]] = times[i]

file1 = open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graphtest1.json", 'w')
json.dump(table, file1, indent=4)
j=0
for i in range(len(table)):
    if sum(table[i]) == 0:
        j+=1
        print(i)
print("total",j)