import sqlite3


class Database:
    def __init__(self):
        self.connection=sqlite3.connect("mpk.db")
        self.cursor=self.connection.cursor()
    def make_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Przystanki(IdP INTEGER NOT NULL CONSTRAINT Przystanki_pk PRIMARY KEY AUTOINCREMENT)''')