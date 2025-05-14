from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'gatitos_clau'

# Configuración de conexión
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
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['contrasenya']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuari WHERE email=%s AND contrasenya=%s", (email, password))
    usuari = cursor.fetchone()
    conn.close()

    if usuari:
        session['usuari'] = usuari
        return redirect(url_for('menu'))
    else:
        return render_template('login.html', error="Credencials incorrectes")

@app.route('/menu')
def menu():
    if 'usuari' not in session:
        return redirect(url_for('index'))
    return render_template('menu.html', usuari=session['usuari'])

@app.route('/llistat')
def llistat():
    if 'usuari' not in session:
        return redirect(url_for('index'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gat")
    gats = cursor.fetchall()
    conn.close()

    return render_template('llistat.html', gats=gats)

@app.route('/afegir', methods=['GET', 'POST'])
def afegir():
    if 'usuari' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        dades = (
            request.form['nom'],
            request.form['edat'],
            request.form['raca'],
            request.form['sexe'],
            request.form.get('esterilitzat') == 'on',
            request.form['data_arribada'],
            request.form['id_centre']
        )

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO gat (nom, edat, raca, sexe, esterilitzat, adoptat, data_arribada, id_centre)
            VALUES (%s, %s, %s, %s, %s, false, %s, %s)
        """, dades)
        conn.commit()
        conn.close()

        return redirect(url_for('llistat'))
    else:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM centre_acollida")
        centres = cursor.fetchall()
        conn.close()
        return render_template('afegir.html', centres=centres)

@app.route('/adopcions', methods=['GET', 'POST'])
def adopcions():
    if 'usuari' not in session or session['usuari']['rol'] != 'admin':
        return redirect(url_for('index'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        cursor.execute("""
            UPDATE gat SET nom=%s, edat=%s, raca=%s, sexe=%s, esterilitzat=%s, adoptat=%s, data_arribada=%s, id_centre=%s
            WHERE id_gat=%s
        """, (
            request.form['nom'],
            request.form['edat'],
            request.form['raca'],
            request.form['sexe'],
            request.form.get('esterilitzat') == 'on',
            request.form.get('adoptat') == 'on',
            request.form['data_arribada'],
            request.form['id_centre'],
            request.form['id_gat']
        ))
        conn.commit()

    cursor.execute("SELECT * FROM gat")
    gats = cursor.fetchall()
    cursor.execute("SELECT * FROM centre_acollida")
    centres = cursor.fetchall()
    conn.close()
    return render_template('adopcions.html', gats=gats, centres=centres)

@app.route('/sortir')
def sortir():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
