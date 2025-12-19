
from .. import db
from sqlalchemy import func
class Squadra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_squadra = db.Column(db.String(150), unique=True)
    numero_componenti = db.Column(db.Integer)
    studenti_componenti = db.relationship("User")
    classe_id = db.Column(db.Integer, db.ForeignKey("classe.id"))
    @classmethod
    def da_id(cls,id:int) -> "Squadra":
       return cls.query.filter_by(id=id).one()
    @classmethod
    def da_nome(cls,nome_classe:str) -> "Squadra":
       return cls.query.filter_by(nome_classe=nome_classe).one()


    def punti_stagione(self,stagione:int) -> float:
        from .cronologia import Cronologia
        from .classe import Classe
        id_utenti_squadra= [studente.id for studente in self.studenti_componenti.all()]

        punti_squadra= db.session.scalar(
            db.select(func.coalesce(func.sum(Cronologia.modifica_punti), 0))
             .where(Cronologia.utente_id.in_(id_utenti_squadra),Cronologia.stagione == stagione))
        punti_compensati = punti_squadra*(Classe.da_id(self.classe_id).massimo_studenti_squadra/len(id_utenti_squadra))
        return punti_compensati


