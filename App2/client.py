import server

usuari = server.iniciar_sessio()
if usuari:
    server.executar_menu(usuari) 
