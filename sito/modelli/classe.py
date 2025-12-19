
from .. import db
class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_classe = db.Column(db.String(150), unique=True)
    massimo_studenti_squadra = db.Column(db.Integer)
    squadre = db.relationship("Squadra")
    studenti = db.relationship("User")
    @classmethod
    def da_id(cls,id:int) -> "Classe":
       return cls.query.filter_by(id=id).one()
    @classmethod
    def da_nome(cls,nome_classe:str) -> "Classe":
       return cls.query.filter_by(nome_classe=nome_classe).one()

