# basedatos.py
import sqlite3

def inicializar_bd():
    conn = sqlite3.connect("refugi_gats.db")
    cur = conn.cursor()

    # Crear tablas
    cur.executescript("""
    DROP TABLE IF EXISTS usuari;
    DROP TABLE IF EXISTS centre_acollida;
    DROP TABLE IF EXISTS gat;
    DROP TABLE IF EXISTS adopcio;

    CREATE TABLE usuari (
        id_usuari INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_complet TEXT,
        email TEXT UNIQUE,
        contrasenya TEXT,
        telefon TEXT,
        rol TEXT
    );

    CREATE TABLE centre_acollida (
        id_centre INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        adreca TEXT
    );

    CREATE TABLE gat (
        id_gat INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        edat INTEGER,
        raça TEXT,
        sexe TEXT,
        esterilitzat BOOLEAN,
        adoptat BOOLEAN,
        data_arribada TEXT,
        id_centre INTEGER,
        FOREIGN KEY(id_centre) REFERENCES centre_acollida(id_centre)
    );

    CREATE TABLE adopcio (
        id_adopcio INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuari INTEGER,
        id_gat INTEGER,
        data_adopcio TEXT,
        estat TEXT,
        comentaris TEXT,
        FOREIGN KEY(id_usuari) REFERENCES usuari(id_usuari),
        FOREIGN KEY(id_gat) REFERENCES gat(id_gat)
    );
    """)

    # Datos de ejemplo
    cur.execute("INSERT INTO centre_acollida (nom, adreca) VALUES (?, ?)", ("Centre Central", "Carrer dels Gats 123"))
    cur.execute("INSERT INTO usuari (nom_complet, email, contrasenya, telefon, rol) VALUES (?, ?, ?, ?, ?)",
                ("Admin", "admin@gats.cat", "1234", "666666666", "admin"))
    cur.execute("INSERT INTO gat (nom, edat, raça, sexe, esterilitzat, adoptat, data_arribada, id_centre) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ("Misu", 2, "Europeu", "F", True, False, "2025-05-01", 1))

    conn.commit()
    conn.close()
    print("Base de dades inicialitzada.")

if __name__ == "__main__":
    inicializar_bd()
