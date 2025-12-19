from . import db
from flask_login import UserMixin
from sqlalchemy import func




class Cronologia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(150))
    stagione = db.Column(db.Integer)
    attivita = db.Column(db.String(150))
    modifica_punti = db.Column(db.Float)
    utente_id = db.Column(db.Integer, db.ForeignKey("user.id"))

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
    classe_id = db.Column(db.Integer, db.ForeignKey("classi.id"))
    squadra_id = db.Column(db.Integer, db.ForeignKey("squadra.id"))

    @classmethod
    def da_id(cls,id:int) -> "Classi":
        return User.query.filter_by(id=id).one()
    @classmethod
    def da_nominativo(cls,nominativo: str) -> "User":
        return User.query.filter_by(nominativo=nominativo).one()
    @classmethod
    def user_da_email(cls,email: str) -> "User":
        return cls.query.filter_by(email=email).one()

    def punti_stagione(self,stagione:int) -> float:
        return db.session.scalar(
            db.select(func.coalesce(func.sum(Cronologia.modifica_punti), 0))
            .where(Cronologia.utente_id== self.id,Cronologia.stagione == stagione)
            )







class Classi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_classe = db.Column(db.String(150), unique=True)
    massimo_studenti_squadra = db.Column(db.Integer)
    squadre = db.relationship("Squadra")
    studenti = db.relationship("User")
    @classmethod
    def da_id(cls,id:int) -> "Classi":
       return cls.query.filter_by(id=id).one()
    @classmethod
    def da_nome(cls,nome_classe:str) -> "Classi":
       return cls.query.filter_by(nome_classe=nome_classe).one()

class Squadra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_squadra = db.Column(db.String(150), unique=True)
    numero_componenti = db.Column(db.Integer)
    studenti_componenti = db.relationship("User")
    classe_id = db.Column(db.Integer, db.ForeignKey("classi.id"))
    @classmethod
    def da_id(cls,id:int) -> "Squadra":
       return cls.query.filter_by(id=id).one()
    @classmethod
    def da_nome(cls,nome_classe:str) -> "Classi":
       return cls.query.filter_by(nome_classe=nome_classe).one()


    def punti_stagione(self,stagione:int) -> float:
        id_utenti_squadra= [studente.id for studente in self.studenti_componenti.all()]

        punti_squadra= db.session.scalar(
            db.select(func.coalesce(func.sum(Cronologia.modifica_punti), 0))
             .where(Cronologia.utente_id.in_(id_utenti_squadra),Cronologia.stagione == stagione))
        punti_compensati = punti_squadra**(Classi.da_id(self.classe_id).massimo_studenti_squadra/len(id_utenti_squadra))
        return punti_compensati



class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_season = db.Column(db.Integer)
    @classmethod
    def _get_singleton(cls) -> "Info":
        info = cls.query.first()
        if info is None:
            info = cls(last_season=1)
            db.session.add(info)
            db.session.commit()
        return info

    @classmethod
    def ottieni_ultima_stagione(cls) -> int:
        return cls._get_singleton().last_season

    @classmethod
    def modifica_ultima_stagione(cls, stagione: int) -> None:
        info = cls._get_singleton()
        info.last_season = stagione
        db.session.commit()

