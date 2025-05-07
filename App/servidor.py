# servidor.py
import socket
import sqlite3
import json

HOST = 'localhost'
PORT = 12345

def manejar_client(conn):
    bd = sqlite3.connect("refugi_gats.db")
    cursor = bd.cursor()

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            peticio = json.loads(data)
            accio = peticio["accio"]

            if accio == "login":
                email = peticio["email"]
                contrasenya = peticio["contrasenya"]
                cursor.execute("SELECT id_usuari, nom_complet, rol FROM usuari WHERE email=? AND contrasenya=?", (email, contrasenya))
                usuari = cursor.fetchone()
                if usuari:
                    resposta = {"estat": "ok", "usuari": {"id": usuari[0], "nom": usuari[1], "rol": usuari[2]}}
                else:
                    resposta = {"estat": "error", "missatge": "Credencials incorrectes"}

            elif accio == "llistar_gats":
                cursor.execute("SELECT nom, edat, raça FROM gat WHERE adoptat=0")
                gats = cursor.fetchall()
                resposta = {"estat": "ok", "gats": gats}

            elif accio == "afegir_gat":
                gat = peticio["gat"]
                cursor.execute("""INSERT INTO gat (nom, edat, raça, sexe, esterilitzat, adoptat, data_arribada, id_centre)
                                  VALUES (?, ?, ?, ?, ?, 0, ?, ?)""",
                               (gat["nom"], gat["edat"], gat["raça"], gat["sexe"], gat["esterilitzat"], gat["data_arribada"], gat["id_centre"]))
                bd.commit()
                resposta = {"estat": "ok", "missatge": "Gat afegit correctament"}

            elif accio == "adoptar_gat":
                id_gat = peticio["id_gat"]
                id_usuari = peticio["id_usuari"]
                data = peticio["data"]
                cursor.execute("INSERT INTO adopcio (id_usuari, id_gat, data_adopcio, estat, comentaris) VALUES (?, ?, ?, ?, ?)",
                               (id_usuari, id_gat, data, "confirmat", ""))
                cursor.execute("UPDATE gat SET adoptat=1 WHERE id_gat=?", (id_gat,))
                bd.commit()
                resposta = {"estat": "ok", "missatge": "Adopció registrada"}

            else:
                resposta = {"estat": "error", "missatge": "Acció desconeguda"}

            conn.send(json.dumps(resposta).encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        bd.close()

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escoltant a {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Connexió de {addr}")
            manejar_client(conn)

if __name__ == "__main__":
    iniciar_servidor()
