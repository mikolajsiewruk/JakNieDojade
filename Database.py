import sqlite3
import os
import json
import logging

# logger configuration
logging.basicConfig(
    filename="adding.log",
    format='%(asctime)s - %(message)s',
    filemode="w",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("mpk.db")
        self.cursor = self.connection.cursor()

    def insert(self, name: str, x: float, y: float, functions: list, district: str):
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

    def get_stops_from_function(self, function: str) -> list:
        """
        Returns all stops that serve a given function.
        :param function: one of [Szkola,Praca,Zakupy,Rozrywka,Restauracje,Spotkania,Zdrowie,Kultura]
        :returns: list of tuples, where each tuple contains stops data.
        """

        query = f"""SELECT IdP,Nazwa,X,Y FROM Przystanki WHERE {function} = 1;"""

        return self.cursor.execute(query).fetchall()

    def add_lines_to_json(self, dir: str):
        """
        Adds lines to a JSON database. Line = {"name", "stops", "times"}.
        """
        used_stops = set()  # used for checking if all stops from the database were used in the process of extraction from html templates
        lines1 = []

        for files in os.listdir(dir):
            path = os.path.join(dir, files)
            file = open(path, "r", encoding="UTF-8")

            name = file.name
            line = []
            stops = []
            times = []
            cur = 0

            for lines in file:  # loop for selection stop names, these names in Wroclaw's MPK webpage are stored in lines where "Przystanek" and "onlyPrint" occur, times are stored with "'" at the end of a line
                if 'Przystanek ' in lines and "onlyPrint" in lines:
                    stops.append(lines[lines.rfind(">") + 2:-1])

                if "Czas przejazdu" in lines and "'" in lines:
                    times.append(int(lines[lines.rfind(">") + 2:-2]) - cur)
                    cur = int(lines[lines.rfind(">") + 2:-2])

            res = []  # stores tuples with the ID and name of a stop
            stop_names = []

            for stop in stops:
                if 'ROD' in stop:  # check for mismatches in the names from the file and the database
                    stop = stop.title()

                if "P&amp;R" in stop:
                    stop = stop.replace("P&amp;R", "PR")

                temp = self.cursor.execute(
                    f"SELECT IdP,Nazwa FROM Przystanki WHERE Nazwa = '{stop}'").fetchone()  # select ID of the stop
                used_stops.add(temp[0])
                res.append(temp[0])
                stop_names.append(temp[1])

            logger.info(
                f"added {name[-13:]},first stop {stop_names[0]} kod {res[0]}, last stop {stop_names[-1]} kod {res[-1]} \nPrzystanki: {stop_names}, Czasy {times}\n Dlugosc przystankow po nazwach {len(stop_names)}, po kodach {len(res)}, dlugosc czasow {len(times)}")  # logging for debugging purposes

            if len(res) - 1 != len(times):
                logger.error(
                    f"Line {name[-13:]} lenghts dont align")  # throw an error in the log to signal that the webpage did not contain all necessary info, important for further graphing

            line.append({"Nazwa": name[-13:], "Przystanki": res, "Czasy": times})
            lines1.append(line)
            # commented for safety
            # json.dump(lines1, open(f"{dir}\\test2.json",'w'), indent=4)  # add a line to json file

        t = self.cursor.execute('SELECT IdP,Nazwa FROM Przystanki').fetchall()
        logger.info(f"used stops {used_stops}\n{len(used_stops)}")
        l = 0  # counter for the amount of stops not used in the making of a graph

        for items in t:
            if items[0] not in used_stops:
                # commented for safety (don't delete my database pls)
                # self.cursor.execute(f"DELETE FROM Przystanki_temp WHERE IdP = '{items[0]}'")  # delete these stops from the database, that were not used in making a graph
                self.connection.commit()
                logger.info(f"Deleted {items[0], items[1]} from the database")
                l += 1
                logger.error(f"{items[0], [items[1]]} not in graph")
        logger.info(f"{l} unused stops in the database")

    def add_info_to_graph(self, dir: str, lines_filepath: str):
        """
        Transfers data from the file with defined lines into adjacency matrix.
        :param dir: output file directory
        :param lines_filepath: path to a JSON file with lines information (Name, stops,times).
        """
        dimensions = len(self.cursor.execute(
            "SELECT IdP FROM Przystanki").fetchall())  # dimensions of the graph matrix = number of stops in the database
        table = [[0] * (dimensions + 1) for _ in range(dimensions + 1)]
        file = open(lines_filepath, 'r')
        data = json.load(file)

        for lines in data:

            stops = lines[0]["Przystanki"]  # get stop IDs and travel times from the file
            times = lines[0]["Czasy"]

            for i in range(len(stops) - 1):
                if times[i] == 0:
                    times[i] = 1  # change zeros to ones (side effect of errors in MPK website)

                if not table[stops[i]][stops[i + 1]] or table[stops[i]][stops[i + 1]] > times[
                    i]:  # if the travel time between stops is shorter than previously, make a switch
                    table[stops[i]][stops[i + 1]] = times[i]
                    table[stops[i + 1]][stops[i]] = times[i]
                    logger.info(f"Added connection between {(stops[i], stops[i + 1])} weight {times[i]}")

        path = os.path.join(dir, "graph.json")
        file1 = open(path, 'w')
        # json.dump(table, file1, indent=4)


if __name__ == '__main__':
    d = Database()
    d.add_info_to_graph("D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\",
                        "D:\PyCharm\PyCharm 2023.2.4\JakNieDojade\Dane\\test2.json")
