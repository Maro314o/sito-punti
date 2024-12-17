from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nominativo = db.Column(
        db.String(150), unique=True
    )  # nome e cognome con la prima lettera maiuscola
    squadra = db.Column(db.String(150))
    password = db.Column(db.String(150))
    punti = db.Column(db.String(150))
    admin_user = db.Column(db.Integer)
    account_attivo = db.Column(db.Integer)
    cronologia_studente = db.relationship("Cronologia")
    classe_id = db.Column(db.Integer, db.ForeignKey("classi.id"))


class Cronologia(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(150))
    stagione = db.Column(db.Integer)
    attivita = db.Column(db.String(150))
    modifica_punti = db.Column(db.Integer)
    punti_cumulativi = db.Column(db.Integer)
    utente_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Classi(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    classe = db.Column(db.String(150), unique=True)
    studenti = db.relationship("User")


class Info(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    last_season = db.Column(db.Integer)
