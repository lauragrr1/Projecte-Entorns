from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'SistemaAdopcions'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('contrasenya', '').strip()

        if not email or not password:
            error = "Cal omplir tots els camps"
        else:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuari WHERE email=%s AND contrasenya=%s", (email, password))
            usuari = cursor.fetchone()
            conn.close()
            if usuari:
                session['usuari'] = usuari
                session['rol'] = usuari['rol']
                return redirect(url_for('menu'))
            else:
                error = "Credencials incorrectes"
    return render_template('login.html', error=error)

@app.route('/menu')
def menu():
    if 'usuari' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html', rol=session.get('rol'), nom_complet=session['usuari']['nom_complet'])

@app.route('/listar_gats')
def listar_gats():
    if 'usuari' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gat")
    gats = cursor.fetchall()
    conn.close()
    return render_template('listar_gats.html', gats=gats)

@app.route('/afegir_gat', methods=['GET', 'POST'])
def afegir_gat():
    if 'usuari' not in session:
        return redirect(url_for('login'))

    error = None
    if request.method == 'POST':
        nom = request.form.get('nom')
        edat = request.form.get('edat')
        raca = request.form.get('raca')
        sexe = request.form.get('sexe')
        esterilitzat = request.form.get('esterilitzat') == 'on'
        data_arribada = request.form.get('data_arribada')
        id_centre = request.form.get('id_centre')

        if not all([nom, edat, raca, sexe, data_arribada, id_centre]):
            error = "Cal omplir tots els camps obligatòriament"
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                sql = """
                    INSERT INTO gat (nom, edat, raca, sexe, esterilitzat, adoptat, data_arribada, id_centre)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (nom, edat, raca, sexe, esterilitzat, False, data_arribada, id_centre))
                conn.commit()
                conn.close()
                # Aquí NO redirigimos para que no te lleve al listar
                return render_template('afegir_gat.html', success="Gat afegit correctament!")
            except mysql.connector.Error as err:
                error = f"Error al insertar gat: {err}"

    # Obtener lista de centros para el select
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM centre_acollida")
    centres = cursor.fetchall()
    conn.close()

    return render_template('afegir_gat.html', centres=centres, error=error)

@app.route('/gestionar_adopcions')
def gestionar_adopcions():
    if 'rol' not in session or session['rol'] != 'admin':
        return "Accés denegat", 403

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gat")
    gats = cursor.fetchall()
    conn.close()
    return render_template('gestionar_adopcions.html', gats=gats)

@app.route('/editar_gat/<int:id_gat>', methods=['GET', 'POST'])
def editar_gat(id_gat):
    if 'rol' not in session or session['rol'] != 'admin':
        return "Accés denegat", 403

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nom = request.form.get('nom')
        edat = request.form.get('edat')
        raca = request.form.get('raca')
        sexe = request.form.get('sexe')
        esterilitzat = request.form.get('esterilitzat') == 'on'
        adoptat = request.form.get('adoptat') == 'on'
        data_arribada = request.form.get('data_arribada')
        id_centre = request.form.get('id_centre')

        if not all([nom, edat, raca, sexe, data_arribada, id_centre]):
            error = "Cal omplir tots els camps obligatòriament"
            cursor.execute("SELECT * FROM gat WHERE id_gat=%s", (id_gat,))
            gat = cursor.fetchone()
            cursor.execute("SELECT * FROM centre_acollida")
            centres = cursor.fetchall()
            conn.close()
            return render_template('editar_gat.html', gat=gat, centres=centres, error=error)

        try:
            sql = """
                UPDATE gat SET nom=%s, edat=%s, raca=%s, sexe=%s, esterilitzat=%s, adoptat=%s, data_arribada=%s, id_centre=%s
                WHERE id_gat=%s
            """
            cursor.execute(sql, (nom, edat, raca, sexe, esterilitzat, adoptat, data_arribada, id_centre, id_gat))
            conn.commit()
            conn.close()
            return redirect(url_for('gestionar_adopcions'))
        except mysql.connector.Error as err:
            error = f"Error actualitzant gat: {err}"
            cursor.execute("SELECT * FROM gat WHERE id_gat=%s", (id_gat,))
            gat = cursor.fetchone()
            cursor.execute("SELECT * FROM centre_acollida")
            centres = cursor.fetchall()
            conn.close()
            return render_template('editar_gat.html', gat=gat, centres=centres, error=error)

    # GET: mostrar formulario con datos actuales
    cursor.execute("SELECT * FROM gat WHERE id_gat=%s", (id_gat,))
    gat = cursor.fetchone()
    cursor.execute("SELECT * FROM centre_acollida")
    centres = cursor.fetchall()
    conn.close()

    return render_template('editar_gat.html', gat=gat, centres=centres)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
