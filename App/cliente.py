# cliente.py
import socket
import json

HOST = 'localhost'
PORT = 12345

def enviar(peticio):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(json.dumps(peticio).encode())
        resposta = s.recv(4096)
        return json.loads(resposta.decode())

def login():
    email = input("Email: ")
    contrasenya = input("Contrasenya: ")
    return enviar({"accio": "login", "email": email, "contrasenya": contrasenya})

def mostrar_menu(usuari):
    while True:
        print("\n--- MENÚ ---")
        print("1. Llistar gats")
        if usuari["rol"] == "admin":
            print("2. Afegir gat")
        print("3. Adoptar gat")
        print("0. Sortir")
        opcio = input("Opció: ")

        if opcio == "1":
            resposta = enviar({"accio": "llistar_gats"})
            for gat in resposta["gats"]:
                print(f"Nom: {gat[0]} | Edat: {gat[1]} | Raça: {gat[2]}")

        elif opcio == "2" and usuari["rol"] == "admin":
            gat = {
                "nom": input("Nom: "),
                "edat": int(input("Edat: ")),
                "raça": input("Raça: "),
                "sexe": input("Sexe: "),
                "esterilitzat": input("Esterilitzat (True/False): ") == "True",
                "data_arribada": input("Data arribada (YYYY-MM-DD): "),
                "id_centre": int(input("ID centre (normalment 1): "))
            }
            resposta = enviar({"accio": "afegir_gat", "gat": gat})
            print(resposta["missatge"])

        elif opcio == "3":
            id_gat = int(input("ID del gat a adoptar: "))
            data = input("Data d'adopció (YYYY-MM-DD): ")
            resposta = enviar({"accio": "adoptar_gat", "id_gat": id_gat, "id_usuari": usuari["id"], "data": data})
            print(resposta["missatge"])

        elif opcio == "0":
            break

        else:
            print("Opció no vàlida.")

if __name__ == "__main__":
    resposta = login()
    if resposta["estat"] == "ok":
        print(f"Benvingut/da, {resposta['usuari']['nom']}!")
        mostrar_menu(resposta["usuari"])
    else:
        print("Error:", resposta["missatge"])
