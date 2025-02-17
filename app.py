from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import qrcode

app = Flask(__name__)

# Configurazione del database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Presenza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

# Creazione del database (solo alla prima esecuzione)
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def home():
    return render_template("form.html")

@app.route("/registrazione", methods=["POST"])
def registrazione():
    nome = request.form["nome"]
    cognome = request.form["cognome"]
    email = request.form["email"]

    # Salviamo i dati nel database
    nuova_presenza = Presenza(nome=nome, cognome=cognome, email=email)
    db.session.add(nuova_presenza)
    db.session.commit()

    return "Registrazione completata! Grazie per la tua partecipazione."

def genera_qr():
    url = "http://localhost:5000"
    qr = qrcode.make(url)
    qr.save("static/qrcode.png")

genera_qr()

if __name__ == "__main__":
    app.run(debug=True)
