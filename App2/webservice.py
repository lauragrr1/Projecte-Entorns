from dao import DAOUsuari, DAOGat, DAOAdopcio
from models import Adopcio
from datetime import date

class Webservice:
    def init(self):
        self.usuari_dao = DAOUsuari()
        self.gat_dao = DAOGat()
        self.adopcio_dao = DAOAdopcio()

    def login(self, email, contrasenya):
        usuari = self.usuari_dao.getUsuariByEmail(email)
        if usuari and usuari.contrasenya == contrasenya:
            return usuari
        return None

    def llistarGats(self):
        return self.gat_dao.getGatsDisponibles()

    def llistarTotsGats(self):
        return self.gat_dao.getAllGats()

    def adoptarGat(self, usuari, nom_gat):
        gat = self.gat_dao.getGatByNom(nom_gat)
        if gat and not gat.adoptat:
            adopcio = Adopcio(None, usuari.id_usuari, gat.id_gat, date.today(), "Pendent", "")
            self.adopcio_dao.crearAdopcio(adopcio)
            self.gat_dao.marcarAdoptat(gat.id_gat)
            return True
        return False

    def llistarAdopcions(self):
        return self.adopcio_dao.getAdopcions()
