import sqlite3
import os
import json

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

    def add_lines_to_json(self,dir):

        lines1 =[]
        for files in os.listdir(dir):
            file = open(f"D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Autobusy\\{files}","r",encoding="UTF-8")

            name = file.name
            line = []
            stops = []
            times = []
            cur = 0

            for lines in file:
                if 'Przystanek' in lines and "onlyPrint" in lines:
                    stops.append(lines[lines.rfind(">") + 2:-1])
                if "Czas przejazdu" in lines and "'" in lines:
                    times.append(int(lines[lines.rfind(">") + 2:-2]) - cur)
                    cur = int(lines[lines.rfind(">") + 2:-2])

            res = []
            for stop in stops:
                if 'ROD' in stop:
                    stop = stop.title()
                temp = self.cursor.execute(f"SELECT IdP,Nazwa FROM Przystanki WHERE Nazwa = '{stop}'").fetchone()
                res.append(temp[0])
            line.append({"Nazwa": name[-13:], "Przystanki": res, "Czasy": times})
            lines1.append(line)
            json.dump(lines1, open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\bus.json",'w'), indent=4)

    def add_info_to_graph(self):
        graph = json.load(open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graph.json",'r'))
        file = open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\bus.json")
        data = json.load(file)
        print(len(graph[0]["graph"]))
        for lines in data:
            print(lines[0]["Nazwa"])
            stops = lines[0]["Przystanki"]
            times = lines[0]["Czasy"]
            print(stops)
            print(times)
            print(len(times),len(stops))
            for i in range(len(stops)-1):
                print(len(times),i)
                print(stops[i])
                print(stops[i+1])
                if graph[0]["graph"][stops[i]][stops[i + 1]] > times[i]:
                    graph[0]["graph"][stops[i]][stops[i + 1]] = times[i]
                    graph[0]["graph"][stops[i + 1]][stops[i]] = times[i]
        file1 = open("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\graph1.json",'w')
        json.dump(graph,file1,indent=4)


d = Database()

d.add_info_to_graph()
