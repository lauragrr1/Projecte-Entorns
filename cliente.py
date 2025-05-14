import socket
import json

HOST = 'localhost'
PORT = 12345

def enviar(peticio):
    """ Envía una petición al servidor y asegura que espera correctamente la respuesta. """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(json.dumps(peticio).encode())

            # Asegurar que la respuesta se recibe correctamente
            resposta = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                resposta += chunk
            
            if not resposta:
                print("⚠️ No s'ha rebut cap resposta del servidor.")
                return {"estat": "error", "missatge": "Sense resposta del servidor"}

            return json.loads(resposta.decode())

    except ConnectionResetError:
        print("❌ Error: La connexió ha estat reiniciada pel servidor.")
        return {"estat": "error", "missatge": "Error de connexió amb el servidor"}

def login():
    print("🔐 LOGIN")
    email = input("Email: ")
    contrasenya = input("Contrasenya: ")
    return enviar({"accio": "login", "email": email, "contrasenya": contrasenya})

def afegir_gat():
    print("\n💼 Afegir Gat")
    nom = input("Nom del gat: ")
    edat = int(input("Edat del gat: "))
    raca = input("Raça del gat: ")
    sexe = input("Sexe del gat (Mascle/Femella): ")
    esterilitzat = input("Esterilitzat? (S/N): ").lower() == 's'
    data_arribada = input("Data d'arribada (YYYY-MM-DD): ")
    id_centre = int(input("ID del centre d'acollida: "))

    gat = {
        "nom": nom,
        "edat": edat,
        "raca": raca,
        "sexe": sexe,
        "esterilitzat": esterilitzat,
        "data_arribada": data_arribada,
        "id_centre": id_centre
    }

    resposta = enviar({"accio": "afegir_gat", "gat": gat, "rol": "admin"})
    print(resposta["missatge"])

def menu():
    print("\n📋 MENÚ PRINCIPAL")
    print("1. Veure llistat de gats (no implementat encara)")
    print("2. Afegir un gat")
    print("3. Sortir")

if __name__ == "__main__":
    resposta = login()
    print(resposta["missatge"])
    if resposta["estat"] == "ok":
        while True:
            menu()
            opcio = input("Escull una opció: ")
            if opcio == "1":
                print("Opció no implementada.")
            elif opcio == "2":
                afegir_gat()
            elif opcio == "3":
                break
            else:
                print("Opció no vàlida.")
