import socket
import json
import sqlite3
import time  # Importar módulo para pausas

HOST = 'localhost'
PORT = 12345

def manejar_client(conn):
    """ Maneja la comunicación con el cliente sin cerrar prematuramente la conexión. """
    with conn:
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    print("⚠️ Connexió buida rebuda, no es tanca immediatament.")
                    conn.send(json.dumps({"estat": "error", "missatge": "Connexió rebuda sense dades."}).encode())
                    continue  # Mantiene el cliente abierto

                print("Dades rebudes:", data)
                peticio = json.loads(data)
                accio = peticio["accio"]

                if accio == "login":
                    email = peticio["email"]
                    contrasenya = peticio["contrasenya"]
                    resposta = login(email, contrasenya)
                    conn.send(json.dumps(resposta).encode())

                    time.sleep(0.5)  # Espera breve antes de cerrar para evitar cortes

                elif accio == "listar_centres":
                    resposta = listar_centres()
                    conn.send(json.dumps(resposta).encode())

                elif accio == "afegir_gat":
                    gat = peticio["gat"]
                    rol = peticio["rol"]
                    if rol == "admin":
                        resposta = afegir_gat(gat)
                        conn.send(json.dumps(resposta).encode())

            except json.JSONDecodeError:
                print("⚠️ Error en el format de la petició.")
                conn.send(json.dumps({"estat": "error", "missatge": "Format de petició incorrecte"}).encode())
                continue  # No cierra el cliente

def login(email, contrasenya):
    conn = sqlite3.connect('gats.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuari WHERE email=? AND contrasenya=?", (email, contrasenya))
    usuari = cur.fetchone()
    conn.close()

    if usuari:
        return {"estat": "ok", "missatge": f"Benvingut/da {usuari[1]}!"}
    else:
        return {"estat": "error", "missatge": "Credencials incorrectes"}

def listar_centres():
    conn = sqlite3.connect('gats.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM centre_acollida")
    centres = cur.fetchall()
    conn.close()
    return {"estat": "ok", "centres": centres}

def afegir_gat(gat):
    conn = sqlite3.connect('gats.db')
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO gat (nom, edat, raca, sexe, esterilitzat, adoptat, data_arribada, id_centre)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (gat["nom"], gat["edat"], gat["raca"], gat["sexe"], gat["esterilitzat"], False, gat["data_arribada"], gat["id_centre"]))
        conn.commit()
        conn.close()
        return {"estat": "ok", "missatge": "Gat afegit correctament."}
    except Exception as e:
        conn.close()
        return {"estat": "error", "missatge": f"Error en afegir el gat: {str(e)}"}

def inicialitzar_base_de_dades():
    """ Crea la base de dades si no existeix. """
    conn = sqlite3.connect('gats.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuari (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            email TEXT UNIQUE,
            contrasenya TEXT
        )
    """)
    conn.commit()
    conn.close()

def servidor():
    """ Inicia el servidor. Maneja excepciones para evitar que se cierre inesperadamente. """
    inicialitzar_base_de_dades()  # Asegurar que la BD esté lista

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            print(f"✅ Servidor vinculat a {HOST}:{PORT}")
            s.listen()
            print("🖥️ Servidor escoltant...")
        except Exception as e:
            print(f"❌ Error en la connexió del servidor: {e}")
            return

        while True:
            try:
                conn, addr = s.accept()
                print(f"🔗 Connexió de {addr}")
                manejar_client(conn)  # Ahora no detiene el servidor si un cliente se desconecta
            except Exception as e:
                print(f"⚠️ Error en la connexió amb el client: {e}")
                continue

servidor()
