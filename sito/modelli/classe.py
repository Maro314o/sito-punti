
from sito.costanti import NOT_AVALIDABLE
from .. import db
class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_classe = db.Column(db.String(150), unique=True)
    massimo_studenti_squadra = db.Column(db.Integer)
    squadre = db.relationship("Squadra",lazy="dynamic")
    studenti = db.relationship("Utente",lazy="dynamic")
    @classmethod
    def da_id(cls,id:int) -> "Classe":
       return cls.query.filter_by(id=id).one()
    @classmethod
    def da_nome(cls,nome_classe:str) -> "Classe":
       return cls.query.filter_by(nome_classe=nome_classe).one()
    @classmethod
    def esiste_da_id(cls,id:int) ->"Classe | None":
       return cls.query.filter_by(id=id).first()
    @classmethod
    def esiste_da_nome(cls,nome_classe:str) -> "Classe | None":
       return cls.query.filter_by(nome_classe=nome_classe).first() 
    @classmethod
    def elenco_classi(cls) -> list["Classe"]:
        """
        Restituisce l'elenco di tutte le classi.
        """
        return cls.query.all()
    @classmethod
    def elenco_classi_studenti(cls) -> list["Classe"]:
        """
        Restituisce l'elenco di tutte le classi degli studenti (escludendo quelle in NOT_AVALIDABLE).
        """
        return cls.query.filter(cls.nome_classe.notin_(NOT_AVALIDABLE)).all()

