# app.py
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connexió MySQL
connexio = mysql.connector.connect(
    host="localhost",
    user="root",
    password="la_teva_contrasenya",
    database="adopta_gatito"
)

cursor = connexio.cursor()

@app.route("/afegir-gat", methods=["GET", "POST"])
def afegir_gat():
    if request.method == "POST":
        nom = request.form["nom"]
        edat = request.form["edat"]
        raca = request.form["raca"]

        sql = "INSERT INTO Gat (nom, edat, raça) VALUES (%s, %s, %s)"
        valors = (nom, edat, raca)
        cursor.execute(sql, valors)
        connexio.commit()
        return "Gat afegit correctament ✅"

    return render_template("afegir_gat.html")

if __name__ == "__main__":
    app.run(debug=True)
