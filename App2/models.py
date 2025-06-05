class Usuari:
    def init(self, id_usuari, nom_complet, email, contrasenya, telefon, rol):
        self.id_usuari = id_usuari
        self.nom_complet = nom_complet
        self.email = email
        self.contrasenya = contrasenya
        self.telefon = telefon
        self.rol = rol

class CentreAcollida:
    def init(self, id_centre, nom, adreca):
        self.id_centre = id_centre
        self.nom = nom
        self.adreca = adreca

class Gat:
    def init(self, id_gat, nom, edat, raça, sexe, esterilitzat, adoptat, data_arribada, id_centre):
        self.id_gat = id_gat
        self.nom = nom
        self.edat = edat
        self.raça = raça
        self.sexe = sexe
        self.esterilitzat = esterilitzat
        self.adoptat = adoptat
        self.data_arribada = data_arribada
        self.id_centre = id_centre

class Adopcio:
    def init(self, id_adopcio, id_usuari, id_gat, data_adopcio, estat, comentaris):
        self.id_adopcio = id_adopcio
        self.id_usuari = id_usuari
        self.id_gat = id_gat
        self.data_adopcio = data_adopcio
        self.estat = estat
        self.comentaris = comentaris
