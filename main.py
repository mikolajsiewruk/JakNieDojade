import sqlite3
import json

# przystanki do bazy danych sql, linie i trasy do pliku json
class Database:
    def __init__(self):
        self.connection=sqlite3.connect("mpk.db")
        self.cursor=self.connection.cursor()
        self.make_tables()
    def make_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Przystanki (IdP INTEGER NOT NULL CONSTRAINT Przystanki_pk PRIMARY KEY AUTOINCREMENT,Nazwa TEXT NOT NULL,X REAL,Y REAL)''')
        self.connection.commit()
d=Database()

s='''<a href="linie-na-przystanku-park-poludniowy-wroclaw">PARK POŁUDNIOWY</a>'''

if 'wroclaw">' in s:
    x=s[s.index(">")+1:]
    print(x[:-4])
stops={}
db=Database()

f = open("Testcases/Przystanki.txt", "r", encoding="utf8")
i=0
l=[]
# dodawanie do bazy danych przystanków, uważać bo sie doda po raz kolejny
for lines in f:
    if 'wroclaw">' in lines:
        i += 1
        x = lines[lines.index(">") + 1:]
        print(x[:-5])
        v=x[:-5]
        v=v.lower()
        v=v.title()
        print(v)
        dict={"id":i,"name":x[:-5]}
        l.append(dict)
        #db.cursor.execute(f"INSERT INTO Przystanki (Nazwa) VALUES ('{v}')")
        #db.connection.commit()

output=open("Dane/stops.json", "w")
json.dump(l,output,indent=4)
