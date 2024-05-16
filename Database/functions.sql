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