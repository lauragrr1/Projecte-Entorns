from flask import Flask, render_template, request, redirect, session, flash
from db_config import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'gatitos-secret'

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasenya = request.form['contrasenya']

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuari WHERE email = %s", (email,))
        usuari = cur.fetchone()
        conn.close()

        if usuari and usuari['contrasenya'] == contrasenya:
            session['usuari'] = usuari
            return redirect('/dashboard')
        else:
            flash("Credencials incorrectes.")
            return redirect('/login')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        contrasenya = request.form['contrasenya']

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO usuari (nom_complet, email, contrasenya, telefon, rol) VALUES (%s, %s, %s, '', 'usuari')",
                        (nom, email, contrasenya))
            conn.commit()
            flash("Usuari registrat correctament.")
        except:
            flash("Aquest email ja està registrat.")
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'usuari' not in session:
        return redirect('/login')

    return render_template('dashboard.html', usuari=session['usuari'])

@app.route('/afegir_gat', methods=['POST'])
def afegir_gat():
    if 'usuari' not in session or session['usuari']['rol'] != 'admin':
        return "No autoritzat", 403

    dades = request.form
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO gat (nom, edat, raca, sexe, esterilitzat, adoptat, data_arribada, id_centre)
        VALUES (%s, %s, %s, %s, %s, 0, %s, %s)
    """, (
        dades['nom'], dades['edat'], dades['raca'], dades['sexe'],
        dades['esterilitzat'], dades['data_arribada'], dades['id_centre']
    ))
    conn.commit()
    conn.close()
    flash("Gat afegit correctament.")
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
