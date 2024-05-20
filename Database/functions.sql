create table Przystanki
(
    IdP         INTEGER
        primary key autoincrement,
    Nazwa       TEXT,
    X           REAL,
    Y           REAL,
    Szkola      INTEGER,
    Praca       INTEGER,
    Zakupy      INTEGER,
    Rozrywka    INTEGER,
    Restauracje INTEGER,
    Spotkania   INTEGER,
    Zdrowie     INTEGER,
    Kultura     INTEGER,
    Osiedle    TEXT
);


CREATE VIEW IF NOT EXISTS Stops_by_area AS
    SELECT Osiedle,COUNT(Osiedle) AS Stops FROM Przystanki
    GROUP BY Osiedle
    ORDER BY Stops DESC;

CREATE TABLE Osiedla
(
    IdO INTEGER PRIMARY KEY  AUTOINCREMENT,
    Name TEXT,
    Area REAL,
    Population REAL
);

CREATE VIEW IF NOT EXISTS Stop_functions AS
    SELECT SUM(iif(Szkola=1,1,0)) AS Szkola, SUM(iif(Praca=1,1,0)) AS Praca,SUM(iif(Zakupy=1,1,0)) AS Zakupy,SUM(iif(Rozrywka=1,1,0)) AS Rozrywka,SUM(iif(Restauracje=1,1,0)) AS Restauracje,SUM(iif(Spotkania=1,1,0)) AS Spotkania,SUM(iif(Zdrowie=1,1,0)) AS Zdrowie,SUM(iif(Kultura=1,1,0)) AS Kultura,SUM(iif(Szkola=0 AND Praca=0 AND Zakupy=0 AND Rozrywka=0 AND Restauracje=0 AND Spotkania=0 AND Zdrowie=0 AND Kultura=0,1,0)) AS Brak FROM Przystanki;

CREATE VIEW IF NOT EXISTS Polozenie AS
    SELECT MIN(X) AS Poludnie, MAX(X) AS Polnoc, MIN(Y) AS Zachod, MAX(Y) AS Wschod FROM Przystanki;


SELECT COUNT(*) AS num_nulls
FROM Przystanki
WHERE Nazwa IS NULL
    OR X IS NULL
    OR Y IS NULL
    OR Przystanki.Szkola IS NULL
    OR Przystanki.Praca IS NULL
    OR Przystanki.Zakupy IS NULL
    OR Przystanki.Rozrywka IS NULL
    OR Przystanki.Restauracje IS NULL
    OR Przystanki.Spotkania IS NULL
    OR Przystanki.Zdrowie IS NULL
    OR Przystanki.Kultura IS NULL
    OR Przystanki.Osiedle IS NULL;

SELECT COUNT(*) AS num_wrong_numbers
FROM Przystanki
WHERE Przystanki.Szkola NOT IN (0,1)
    OR Przystanki.Praca NOT IN (0,1)
    OR Przystanki.Zakupy NOT IN (0,1)
    OR Przystanki.Rozrywka NOT IN (0,1)
    OR Przystanki.Restauracje NOT IN (0,1)
    OR Przystanki.Spotkania NOT IN (0,1)
    OR Przystanki.Zdrowie NOT IN (0,1)
    OR Przystanki.Kultura NOT IN (0,1);


SELECT COUNT(*) AS num_useless_stops
FROM Przystanki
WHERE Przystanki.Szkola = 0
    AND Przystanki.Praca = 0
    AND Przystanki.Zakupy = 0
    AND Przystanki.Rozrywka = 0
    AND Przystanki.Restauracje = 0
    AND Przystanki.Spotkania = 0
    AND Przystanki.Zdrowie = 0
    AND Przystanki.Kultura = 0;

