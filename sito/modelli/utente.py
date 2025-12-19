from sito.misc_utils_funcs.parse_utils import converti_a_unix
from sito.modelli.cronologia import Cronologia
from .. import db
from sqlalchemy import func
from flask_login import UserMixin

class Utente(db.Model, UserMixin):
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
    def da_id(cls,id:int) -> "Utente":
        return Utente.query.filter_by(id=id).one()
    @classmethod
    def da_nominativo(cls,nominativo: str) -> "Utente":
        return Utente.query.filter_by(nominativo=nominativo).one()
    @classmethod
    def da_email(cls,email: str) -> "Utente":
        return cls.query.filter_by(email=email).one()

    def punti_stagione(self,stagione:int) -> float:
        from .cronologia import Cronologia
        return db.session.scalar(
            db.select(func.coalesce(func.sum(Cronologia.modifica_punti), 0))
            .where(Cronologia.utente_id== self.id,Cronologia.stagione == stagione)
            )
    from .cronologia import Cronologia
    def elenco_cronologia_stagione(self,stagione:int,cronologicamente:bool = True) -> list["Cronologia"]:
        cronologia =  self.cronologia_studente.filter_by(stagione=stagione).all()
        if cronologicamente:
            cronologia= sorted(cronologia, key=lambda evento: converti_a_unix(evento.data))
        return cronologia

        
    @classmethod
    def elenco_utenti(cls) -> list["Utente"]:
        """
        Restituisce l'elenco di tutti gli utenti.
        """
        return cls.query.all()


    @classmethod
    def elenco_studenti(cls) -> list["Utente"]:
        """
        Restituisce l'elenco di tutti gli studenti.
        """
        return cls.query.filter_by(admin_user=False).all()


    @classmethod
    def elenco_admin(cls) -> list["Utente"]:
        """
        Restituisce l'elenco di tutti gli admin.
        """
        return cls.query.filter_by(admin_user=True).all()


    @classmethod
    def elenco_studenti_registrati(cls) -> list["Utente"]:
        """
        Restituisce l'elenco di tutti gli studenti registrati.
        """
        return cls.query.filter_by(admin_user=False, account_attivo=True).all()


    @classmethod
    def elenco_studenti_non_registrati(cls) -> list["Utente"]:
        """
        Restituisce l'elenco di tutti gli studenti non registrati.
        """
        return cls.query.filter_by(admin_user=False, account_attivo=False).all()

