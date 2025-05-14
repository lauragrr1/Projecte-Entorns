import sqlite3

conn = sqlite3.connect("gats.db")
cur = conn.cursor()

# Eliminar las tablas existentes si existen (para asegurarnos de que se recrean correctamente)
cur.execute("DROP TABLE IF EXISTS gat")
cur.execute("DROP TABLE IF EXISTS usuari")
cur.execute("DROP TABLE IF EXISTS centre_acollida")
cur.execute("DROP TABLE IF EXISTS adopcio")

# Crear las tablas nuevamente con las columnas correctas

cur.execute("""
CREATE TABLE IF NOT EXISTS usuari (
    id_usuari INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_complet TEXT,
    email TEXT UNIQUE,
    contrasenya TEXT,
    telefon TEXT,
    rol TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS centre_acollida (
    id_centre INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    adreca TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS gat (
    id_gat INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    edat INTEGER,
    raca TEXT,  -- Aseguramos que la columna 'raca' existe
    sexe TEXT,
    esterilitzat BOOLEAN,
    adoptat BOOLEAN,
    data_arribada TEXT,
    id_centre INTEGER,
    FOREIGN KEY(id_centre) REFERENCES centre_acollida(id_centre)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS adopcio (
    id_adopcio INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuari INTEGER,
    id_gat INTEGER,
    data_adopcio TEXT,
    estat TEXT,
    comentaris TEXT,
    FOREIGN KEY(id_usuari) REFERENCES usuari(id_usuari),
    FOREIGN KEY(id_gat) REFERENCES gat(id_gat)
)
""")

# Crear un usuari administrador per poder fer login
cur.execute("INSERT OR IGNORE INTO usuari (email, contrasenya, nom_complet, telefon, rol) VALUES (?, ?, ?, ?, ?)",
            ("admin@gmail.com", "1234", "Administrador", "123456789", "admin"))

# Insertar algunos centros de acogida y gatos para probar
cur.execute("INSERT OR IGNORE INTO centre_acollida (nom, adreca) VALUES (?, ?)", ("Centre d'Acollida 1", "Carrer 1, Ciutat 1"))
cur.execute("INSERT OR IGNORE INTO centre_acollida (nom, adreca) VALUES (?, ?)", ("Centre d'Acollida 2", "Carrer 2, Ciutat 2"))

# Insertar algunos gatos
cur.executemany("""
    INSERT OR IGNORE INTO gat (nom, edat, raca, sexe, esterilitzat, adoptat, data_arribada, id_centre)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ("Miu", 1, "Carrer", "Mascle", True, False, "2020-10-10", 1),
    ("Luna", 2, "Persa", "Femella", True, False, "2021-02-15", 2),
    ("Rex", 3, "Siamès", "Mascle", False, False, "2022-01-20", 1)
])

conn.commit()
conn.close()

print("Base de dades creada correctament.")
