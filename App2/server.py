from webservice import Webservice
from models import Gat, Adopcio
from datetime import datetime

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
    print("\n--- Menú Admin ---")
    print("1. Llistar Gats")
    print("2. Gestionar Adopcions")
    print("3. Gestionar Gats")
    print("4. Sortir")

def mostrar_menu_usuari():
    print("\n--- Menú Usuari ---")
    print("1. Llistar Gats")
    print("2. Adoptar Gat")
    print("3. Sortir")

def imprimir_gat_complet(gat):
    print(f"ID: {gat.id_gat}, Nom: {gat.nom}, Edat: {gat.edat}, Raça: {gat.raça}, Sexe: {gat.sexe}, "
          f"Esterilitzat: {'Sí' if gat.esterilitzat else 'No'}, Adoptat: {'Sí' if gat.adoptat else 'No'}, "
          f"Data Arribada: {gat.data_arribada}, Centre: {gat.id_centre}")


def modificar_adopcio():
    adopcions = ws.llistarAdopcions()
    if not adopcions:
        print("No hi ha adopcions per gestionar.")
        return
    for a in adopcions:
        print(f"ID: {a.id_adopcio}, Gat ID: {a.id_gat}, Usuari ID: {a.id_usuari}, Estat: {a.estat}, Comentaris: {a.comentaris}")
    try:
        id_adopcio = int(input("Introdueix l'ID de l'adopcio a modificar: "))
    except ValueError:
        print("ID invàlid.")
        return
    adopcio_sel = next((a for a in adopcions if a.id_adopcio == id_adopcio), None)
    if not adopcio_sel:
        print("Adopcio no trobada.")
        return
    try:
        nou_usuari_id = int(input("Nou ID d'usuari (qui adopta): "))
    except ValueError:
        print("ID invàlid.")
        return
    nou_estat = input("Nou estat: ")
    nous_comentaris = input("Nous comentaris: ")
    adopcio_sel.id_usuari = nou_usuari_id
    adopcio_sel.estat = nou_estat
    adopcio_sel.comentaris = nous_comentaris
    ws.actualitzarAdopcio(adopcio_sel)
    print("Adopció actualitzada.")

def gestionar_gats():
    while True:
        print("\n--- Gestió Gats ---")
        print("1. Crear Gat")
        print("2. Modificar Gat")
        print("3. Eliminar Gat")
        print("4. Llistar Gats")
        print("5. Tornar enrere")
        opcio = input("Opció: ")
        if opcio == "1":
            nom = input("Nom: ")
            edat = input("Edat: ")
            raça = input("Raça: ")
            sexe = input("Sexe: ")
            esterilitzat = input("Esterilitzat (True/False): ").lower() == "true"
            adoptat = False
            data_arribada = input("Data arribada (YYYY-MM-DD): ")
            id_centre = input("ID centre acollida: ")
            gat = Gat(None, nom, edat, raça, sexe, esterilitzat, adoptat, data_arribada, id_centre)
            ws.crearGat(gat)
            print("Gat creat correctament.")
        elif opcio == "2":
            try:
                id_gat = int(input("ID del gat a modificar: "))
            except ValueError:
                print("ID invàlid.")
                continue
            gat = ws.getGatById(id_gat)
            if not gat:
                print("Gat no trobat.")
                continue
            print("Deixa en blanc per mantenir el valor actual.")
            nom = input(f"Nom ({gat.nom}): ") or gat.nom
            edat = input(f"Edat ({gat.edat}): ") or gat.edat
            raça = input(f"Raça ({gat.raça}): ") or gat.raça
            sexe = input(f"Sexe ({gat.sexe}): ") or gat.sexe
            esterilitzat_input = input(f"Esterilitzat ({gat.esterilitzat}): ")
            esterilitzat = gat.esterilitzat if esterilitzat_input == "" else esterilitzat_input.lower() == "true"
            adoptat_input = input(f"Adoptat ({gat.adoptat}): ")
            adoptat = gat.adoptat if adoptat_input == "" else adoptat_input.lower() == "true"
            data_arribada = input(f"Data arribada ({gat.data_arribada}): ") or gat.data_arribada
            id_centre = input(f"ID centre ({gat.id_centre}): ") or gat.id_centre

            gat.nom = nom
            gat.edat = edat
            gat.raça = raça
            gat.sexe = sexe
            gat.esterilitzat = esterilitzat
            gat.adoptat = adoptat
            gat.data_arribada = data_arribada
            gat.id_centre = id_centre
            ws.actualitzarGat(gat)
            print("Gat actualitzat correctament.")
        elif opcio == "3":
            try:
                id_gat = int(input("ID del gat a eliminar: "))
            except ValueError:
                print("ID invàlid.")
                continue
            gat = ws.getGatById(id_gat)
            if not gat:
                print("Gat no trobat.")
                continue
            ws.eliminarGat(id_gat)
            print("Gat eliminat correctament.")
        elif opcio == "4":
            gats = ws.llistarTotsGats()
            for gat in gats:
                imprimir_gat_complet(gat)
        elif opcio == "5":
            break
        else:
            print("Opció invàlida.")

def executar_menu(usuari):
    while True:
        if usuari.rol == "admin":
            mostrar_menu_admin()
            opcio = input("Opció: ")
            if opcio == "1":
                gats = ws.llistarTotsGats()
                for gat in gats:
                    imprimir_gat_complet(gat)
            elif opcio == "2":
                modificar_adopcio()
            elif opcio == "3":
                gestionar_gats()
            elif opcio == "4":
                break
            else:
                print("Opció invàlida.")
        else:
            mostrar_menu_usuari()
            opcio = input("Opció: ")
            if opcio == "1":
                gats = ws.llistarGats()
                for gat in gats:
                    imprimir_gat_complet(gat)
            elif opcio == "2":
                nom = input("Nom del gat que vols adoptar: ")
                if ws.adoptarGat(usuari, nom):
                    print("Adopció registrada amb èxit.")
                else:
                    print("Error: el gat no existeix o ja està adoptat.")
            elif opcio == "3":
                break
            else:
                print("Opció invàlida.")
