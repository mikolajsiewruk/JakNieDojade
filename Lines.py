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
output=open("Dane/lines.json", "w")
d=os.getcwd()
dir=os.listdir(f"{d}\\Materials")
lines1=[]
files=[file for file in dir]

def add_lines():
    """
    Add lines to JSON file. Stop ids and time from stop to stop.
    :return:
    """
    for file in files:
        f = open(f"Materials\{file}","r", encoding="utf-8")
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
        res=[]
        for stop in stops:
            res.append(cursor.execute(f"SELECT IdP FROM Przystanki WHERE Nazwa = '{stop}'").fetchone()[0])
        line.append({"Nazwa":name,"Przystanki":res,"Czasy":times})
        lines1.append(line)
    # json.dump(lines1,output,indent=4) dont use until complete
