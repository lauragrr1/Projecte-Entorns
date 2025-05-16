import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Crea un test client y activa modo testing
        self.app = app.test_client()
        self.app.testing = True

    def test_llistar_gats_access_with_login(self):
        # Simula una sessió iniciada
        with self.app.session_transaction() as sess:
            sess['usuari'] = {'id': 1, 'nom_complet': 'Test Usuari'}
            sess['rol'] = 'usuari'

        # Fa una petició GET a /listar_gats
        response = self.app.get('/listar_gats')

        # Comprova que retorna HTTP 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Llista de Gats', response.data)  # Opcional: comprova que apareix text a la pàgina

    def test_llistar_gats_redirects_without_login(self):
        # Sense login ha de redirigir (302) al login
        response = self.app.get('/listar_gats', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()
