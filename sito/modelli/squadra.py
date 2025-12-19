
from sito.costanti import NOT_AVALIDABLE
from .. import db
from sqlalchemy import func
class Squadra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_squadra = db.Column(db.String(150), unique=True)
    numero_componenti = db.Column(db.Integer)
    studenti_componenti = db.relationship("Utente",lazy="dynamic")
    classe_id = db.Column(db.Integer, db.ForeignKey("classe.id"))
    @classmethod
    def da_id(cls,id:int) -> "Squadra":
       return cls.query.filter_by(id=id).one()
    @classmethod
    def da_nome(cls,nome_squadra:str) -> "Squadra":
       return cls.query.filter_by(nome_squadra=nome_squadra).one()


    def punti_stagione(self,stagione:int) -> float:
        from .cronologia import Cronologia
        from .classe import Classe
        id_utenti_squadra= [studente.id for studente in self.studenti_componenti.all()]

        punti_squadra= db.session.scalar(
            db.select(func.coalesce(func.sum(Cronologia.modifica_punti), 0))
             .where(Cronologia.utente_id.in_(id_utenti_squadra),Cronologia.stagione == stagione))
        punti_compensati = punti_squadra*(Classe.da_id(self.classe_id).massimo_studenti_squadra/len(id_utenti_squadra))
        return punti_compensati
    @classmethod
    def elenco_squadre(cls) -> list["Squadra"]:
        """
        Restituisce l'elenco di tutte le squadre.
        """
        return cls.query.all()
    @classmethod
    def elenco_squadre_studenti(cls) -> list["Squadra"]:
        """
        Restituisce l'elenco di tutte le squadre degli studenti (escludendo quelle in NOT_AVALIDABLE).
        """
        return cls.query.filter(cls.nome_squadra.notin_(NOT_AVALIDABLE)).all()



