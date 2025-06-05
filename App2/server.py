server.py: from webservice import Webservice
ws = Webservice()

def iniciar_sessio():
    email = input("Email: ")
    contrasenya = input("Contrasenya: ")
    usuari = ws.login(email, contrasenya)
    if usuari:
        print(f"Benvingut, {usuari.nom_complet}!")
        return usuari
    else:
        print("Credencials incorrectes.")
        return None

def mostrar_menu_admin():
    print("1. Llistar Gats")
    print("2. Gestionar Adopcions")
    print("3. Gestionar Gats")
    print("4. Sortir")

def mostrar_menu_usuari():
    print("1. Llistar Gats")
    print("2. Adoptar Gat")
    print("3. Sortir")

def executar_menu(usuari):
    while True:
        if usuari.rol == "admin":
            mostrar_menu_admin()
            opcio = input("Opció: ")
            if opcio == "1":
                gats = ws.llistarGats()
                for gat in gats:
                    print(f"{gat.nom}, {gat.edat} anys, raça: {gat.raça}")
            elif opcio == "2":
                adopcions = ws.llistarAdopcions()
                for a in adopcions:
                    print(f"Adopcio {a.id_adopcio}: Gat {a.id_gat}, Usuari {a.id_usuari}, Estat: {a.estat}")
            elif opcio == "3":
                gats = ws.llistarTotsGats()
                for gat in gats:
                    print(f"ID: {gat.id_gat}, Nom: {gat.nom}, Adoptat: {'Sí' if gat.adoptat else 'No'}")
            elif opcio == "4":
                break
        else:
            mostrar_menu_usuari()
            opcio = input("Opció: ")
            if opcio == "1":
                gats = ws.llistarGats()
                for gat in gats:
                    print(f"{gat.nom}, {gat.edat} anys, raça: {gat.raça}")
            elif opcio == "2":
                nom = input("Nom del gat que vols adoptar: ")
                if ws.adoptarGat(usuari, nom):
                    print("Adopció registrada amb èxit.")
                else:
                    print("Error: el gat no existeix o ja està adoptat.")
            elif opcio == "3":
                break
