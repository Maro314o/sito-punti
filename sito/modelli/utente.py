from .. import db
from sqlalchemy import func
from flask_login import UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nominativo = db.Column(
        db.String(150), unique=True
    )  #cognome e nome  con la prima lettera maiuscola
    squadra = db.Column(db.String(150))
    password = db.Column(db.String(150))
    admin_user = db.Column(db.Integer)
    account_attivo = db.Column(db.Integer)
    cronologia_studente = db.relationship("Cronologia")
    classe_id = db.Column(db.Integer, db.ForeignKey("classe.id"))
    squadra_id = db.Column(db.Integer, db.ForeignKey("squadra.id"))

    @classmethod
    def da_id(cls,id:int) -> "User":
        return User.query.filter_by(id=id).one()
    @classmethod
    def da_nominativo(cls,nominativo: str) -> "User":
        return User.query.filter_by(nominativo=nominativo).one()
    @classmethod
    def user_da_email(cls,email: str) -> "User":
        return cls.query.filter_by(email=email).one()

    def punti_stagione(self,stagione:int) -> float:
        from .cronologia import Cronologia
        return db.session.scalar(
            db.select(func.coalesce(func.sum(Cronologia.modifica_punti), 0))
            .where(Cronologia.utente_id== self.id,Cronologia.stagione == stagione)
            )

