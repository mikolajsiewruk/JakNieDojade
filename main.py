import sqlite3

### zmienić to na nierelacyjna baze !!!! ### MONGO_DB
class Database:
    def __init__(self):
        self.connection=sqlite3.connect("mpk.db")
        self.cursor=self.connection.cursor()
        self.make_tables()
    def make_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Przystanki(IdP INTEGER NOT NULL CONSTRAINT Przystanki_pk PRIMARY KEY AUTOINCREMENT,Nazwa TEXT NOT NULL,X REAL,Y REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Linie(IdL INTEGER NOT NULL CONSTRAINT Linie_pk PRIMARY KEY AUTOINCREMENT,Symbol TEXT NOT NULL, Trasa ''')
        self.connection.commit()