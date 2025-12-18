from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nominativo = db.Column(
        db.String(150), unique=True
    )  #cognome e nome  con la prima lettera maiuscola
    squadra = db.Column(db.String(150))
    password = db.Column(db.String(150))
    punti = db.Column(db.String(150))
    admin_user = db.Column(db.Integer)
    account_attivo = db.Column(db.Integer)
    cronologia_studente = db.relationship("Cronologia")
    classe_id = db.Column(db.Integer, db.ForeignKey("classi.id"))
    squadra_id = db.Column(db.Integer, db.ForeignKey("squadra.id"))


class Cronologia(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(150))
    stagione = db.Column(db.Integer)
    attivita = db.Column(db.String(150))
    modifica_punti = db.Column(db.Float)
    punti_cumulativi = db.Column(db.Float)
    utente_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Classi(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    classe = db.Column(db.String(150), unique=True)
    massimo_studenti_squadra = db.Column(db.Integer)
    squadre = db.relationship("Squadra")
    studenti = db.relationship("User")


class Squadra(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome_squadra = db.Column(db.String(150), unique=True)
    numero_componenti = db.Column(db.Integer)
    punti_reali = db.Column(db.String(150))
    punti_compensati = db.Column(db.String(150))
    studenti_componenti = db.relationship("User")
    classe_id = db.Column(db.Integer, db.ForeignKey("classi.id"))


class Info(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    last_season = db.Column(db.Integer)
