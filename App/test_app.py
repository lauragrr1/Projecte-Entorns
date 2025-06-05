test_app.py: import unittest
from datetime import date
from webservice import Webservice
from models import Gat, Adopcio

class TestSistemaAdopcio(unittest.TestCase):
    def setUp(self):
        self.ws = Webservice()

        # Crear usuari de test (si no existe)
        self.test_email = "test@exemple.com"
        self.test_password = "1234"
        usuari = self.ws.login(self.test_email, self.test_password)
        if not usuari:
            # Inserta usuari manualment (no hay mètode crearUsuari)
            import mysql.connector
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="sistemaAdopciones")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuari (nom_complet, email, contrasenya, telefon, rol) VALUES (%s, %s, %s, %s, %s)",
                ("Usuari Test", self.test_email, self.test_password, "123456789", "usuari")
            )
            conn.commit()
            conn.close()

        self.usuari = self.ws.login(self.test_email, self.test_password)
        self.assertIsNotNone(self.usuari, "No s'ha pogut iniciar sessió amb l'usuari de test.")

    def test_llistar_gats_disponibles(self):
        gats = self.ws.llistarGats()
        self.assertIsInstance(gats, list)

    def test_crear_i_modificar_gat(self):
        gat = Gat(None, "GatTest", 2, "Europeu", "M", True, False, date.today(), 1)
        self.ws.crearGat(gat)

        # Recuperar el gat per nom
        recuperat = self.ws.getGatByNom("GatTest")
        self.assertIsNotNone(recuperat)
        self.assertEqual(recuperat.nom, "GatTest")

        # Modificar edat i esterilitzat
        recuperat.edat = 3
        recuperat.esterilitzat = False
        self.ws.actualitzarGat(recuperat)

        modificat = self.ws.getGatById(recuperat.id_gat)
        self.assertEqual(modificat.edat, 3)
        self.assertFalse(modificat.esterilitzat)

    def test_adoptar_gat(self):
        gat = self.ws.getGatById("GatTest")
        if gat.adoptat:
            self.fail("El gat ja està adoptat, no es pot provar adopció.")
        resultat = self.ws.adoptarGat(self.usuari, "GatTest")
        self.assertTrue(resultat)

        gat_actualitzat = self.ws.getGatByNom("GatTest")
        self.assertTrue(gat_actualitzat.adoptat)

    def test_llistar_i_modificar_adopcio(self):
        adopcions = self.ws.llistarAdopcions()
        self.assertGreaterEqual(len(adopcions), 1)

        adopcio = next((a for a in adopcions if a.id_usuari == self.usuari.id_usuari), None)
        if adopcio:
            adopcio.estat = "Acceptada"
            adopcio.comentaris = "Tot correcte"
            self.ws.actualitzarAdopcio(adopcio)

            actualitzada = next((a for a in self.ws.llistarAdopcions() if a.id_adopcio == adopcio.id_adopcio), None)
            self.assertEqual(actualitzada.estat, "Acceptada")
            self.assertEqual(actualitzada.comentaris, "Tot correcte")

    def tearDown(self):
        # Eliminar dades de test
        import mysql.connector
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="sistemaAdopciones")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM adopcio WHERE id_usuari = %s", (self.usuari.id_usuari,))
        cursor.execute("DELETE FROM gat WHERE nom = 'GatTest'")
        cursor.execute("DELETE FROM usuari WHERE email = %s", (self.test_email,))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    unittest.main()
