
from .. import db
class Cronologia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(150))
    stagione = db.Column(db.Integer)
    attivita = db.Column(db.String(150))
    modifica_punti = db.Column(db.Float)
    utente_id = db.Column(db.Integer, db.ForeignKey("user.id"))

