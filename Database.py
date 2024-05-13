import sqlite3

class Database:
    def __init__(self):
        self.connection=sqlite3.connect("mpk.db")
        self.cursor=self.connection.cursor()

    def insert(self,name: str,x:float,y:float,functions:list,district:str):
        """
        Inserts a public transportation stop to the database.
        :param name: name of a stop.
        :param x: x coordinate.
        :param y: y coordinate.
        :param functions: list [school,work,shopping,leisure,food,meetings,medical,culture], each parameter should be a 1 if stop serves this purpose and 0 if it does not.
        :param district: a district in which the stop is located.
        """

        query = f"""INSERT INTO Przystanki (VALUES {name},{x},{y},{functions[0]},{functions[1]},{functions[2]},{functions[3]},{functions[4]},{functions[5]},{functions[6]},{functions[7]});"""
        self.cursor.execute(query)
        self.connection.commit()

    def get_stops_from_function(self,function:str)->list:
        """
        Returns all stops that serve a given function.
        :param function: one of [Szkola,Praca,Zakupy,Rozrywka,Restauracje,Spotkania,Zdrowie,Kultura]
        :returns: list of tuples, where each tuple contains stops data.
        """

        query = f"""SELECT IdP,Nazwa,X,Y FROM Przystanki WHERE {function} = 1;"""

        return self.cursor.execute(query).fetchall()

for i in range(112,153):
    f = open(f"D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Autobusy\\Linia_{i}.txt","wb")