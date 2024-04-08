import json
import sqlite3
import  os

connection=sqlite3.connect('mpk.db')
cursor=connection.cursor()
temp = cursor.execute("SELECT Nazwa FROM Przystanki").fetchall()
l=[]
for t in temp:
    a=list(t)
    a[0]=a[0].lower()
    a[0]=a[0].title()
    l.append(a[0])
output=open("lines.json","w")
d=os.getcwd()
dir=os.listdir(f"{d}\\Materials")
lines1=[]
for files in dir:

    f = open(f"Materials\{files}","r", encoding="utf-8")
    name=f.name
    line=[]
    stops=[]
    times=[]
    cur=0
    for lines in f:
        if 'Przystanek' in lines:
            print(lines[lines.rfind(">")+2:])
            stops.append(lines[lines.rfind(">")+2:-1])
        if "Czas przejazdu" in lines and "'" in lines:
            print(lines[lines.rfind(">")+2:-2])
            times.append(int(lines[lines.rfind(">")+2:-2])-cur)
            cur=int(lines[lines.rfind(">")+2:-2])
    print(stops)
    print(times)
    res=[]
    for stop in stops:
        print(stop)
        print(cursor.execute(f"SELECT IdP FROM Przystanki WHERE Nazwa = '{stop}'").fetchone()[0])
        res.append(cursor.execute(f"SELECT IdP FROM Przystanki WHERE Nazwa = '{stop}'").fetchone()[0])
    print(res)
    line.append({"Nazwa":name,"Przystanki":res,"Czasy":times})
    lines1.append(line)
json.dump(lines1,output,indent=4)
# and lines[lines.index(">")+1:] in l: