from db_config import get_connection
from models import *

class DAOUsuari:
    def getUsuariByEmail(self, email):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuari WHERE email = %s", (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuari(*row)
        return None

class DAOCentreAcollida:
    def getCentreById(self, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM centre_acollida WHERE id_centre = %s", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return CentreAcollida(*row)
        return None

class DAOGat:
    def getGatsDisponibles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gat WHERE adoptat = FALSE")
        rows = cursor.fetchall()
        conn.close()
        return [Gat(*row) for row in rows]

    def getGatByNom(self, nom):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gat WHERE nom = %s", (nom,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Gat(*row)
        return None

    def marcarAdoptat(self, id_gat):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE gat SET adoptat = TRUE WHERE id_gat = %s", (id_gat,))
        conn.commit()
        conn.close()

    def getAllGats(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gat")
        rows = cursor.fetchall()
        conn.close()
        return [Gat(*row) for row in rows]

    def crearGat(self, gat):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO gat (nom, edat, raça, sexe, esterilitzat, adoptat, data_arribada, id_centre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (gat.nom, gat.edat, gat.raça, gat.sexe, gat.esterilitzat, gat.adoptat, gat.data_arribada, gat.id_centre)
        )
        conn.commit()
        conn.close()

    def actualitzarGat(self, gat):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE gat SET nom=%s, edat=%s, raça=%s, sexe=%s, esterilitzat=%s, adoptat=%s, data_arribada=%s, id_centre=%s WHERE id_gat=%s",
            (gat.nom, gat.edat, gat.raça, gat.sexe, gat.esterilitzat, gat.adoptat, gat.data_arribada, gat.id_centre, gat.id_gat)
        )
        conn.commit()
        conn.close()

    def eliminarGat(self, id_gat):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gat WHERE id_gat = %s", (id_gat,))
        conn.commit()
        conn.close()

class DAOAdopcio:
    def crearAdopcio(self, adopcio):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO adopcio (id_usuari, id_gat, data_adopcio, estat, comentaris) VALUES (%s, %s, %s, %s, %s)",
            (adopcio.id_usuari, adopcio.id_gat, adopcio.data_adopcio, adopcio.estat, adopcio.comentaris)
        )
        conn.commit()
        conn.close()

    def getAdopcions(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM adopcio")
        rows = cursor.fetchall()
        conn.close()
        return [Adopcio(*row) for row in rows]

    def actualitzarAdopcio(self, adopcio):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE adopcio SET id_usuari=%s, id_gat=%s, data_adopcio=%s, estat=%s, comentaris=%s WHERE id_adopcio=%s",
            (adopcio.id_usuari, adopcio.id_gat, adopcio.data_adopcio, adopcio.estat, adopcio.comentaris, adopcio.id_adopcio)
        )
        conn.commit()
        conn.close()
