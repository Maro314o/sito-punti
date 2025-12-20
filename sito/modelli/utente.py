from sito.misc_utils_funcs.parse_utils import converti_a_unix
from sito.modelli.cronologia import Cronologia
from .. import db
from sqlalchemy import func
from flask_login import UserMixin


class Utente(db.Model, UserMixin):
    """
    Modello ORM che rappresenta un utente del sistema.

    Può essere uno studente o un amministratore e contiene
    informazioni anagrafiche, di autenticazione e relazioni
    con la cronologia delle attività.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nominativo = db.Column(
        db.String(150), unique=True
    )  # Cognome e nome con la prima lettera maiuscola
    squadra = db.Column(db.String(150))
    password = db.Column(db.String(150))
    admin_user = db.Column(db.Integer)
    account_attivo = db.Column(db.Integer)

    cronologia_studente = db.relationship("Cronologia", lazy="dynamic")

    classe_id = db.Column(db.Integer, db.ForeignKey("classe.id"))
    squadra_id = db.Column(db.Integer, db.ForeignKey("squadra.id"))

    @classmethod
    def da_id(cls, id: int) -> "Utente":
        """
        Restituisce un utente a partire dal suo ID.

        :param id: ID dell'utente
        :return: Istanza di Utente
        :raises sqlalchemy.exc.NoResultFound: se l'utente non esiste
        """
        return cls.query.filter_by(id=id).one()

    @classmethod
    def da_nominativo(cls, nominativo: str) -> "Utente":
        """
        Restituisce un utente a partire dal nominativo.

        :param nominativo: Cognome e nome dell'utente
        :return: Istanza di Utente
        :raises sqlalchemy.exc.NoResultFound: se l'utente non esiste
        """
        return cls.query.filter_by(nominativo=nominativo).one()

    @classmethod
    def da_email(cls, email: str) -> "Utente":
        """
        Restituisce un utente a partire dall'indirizzo email.

        :param email: Email dell'utente
        :return: Istanza di Utente
        :raises sqlalchemy.exc.NoResultFound: se l'utente non esiste
        """
        return cls.query.filter_by(email=email).one()

    @classmethod
    def esiste_da_id(cls, id: int) -> "Utente | None":
        """
        Verifica l'esistenza di un utente dato l'ID.

        :param id: ID dell'utente
        :return: Utente se esiste, altrimenti None
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def esiste_da_nominativo(cls, nominativo: str) -> "Utente | None":
        """
        Verifica l'esistenza di un utente dato il nominativo.

        :param nominativo: Cognome e nome dell'utente
        :return: Utente se esiste, altrimenti None
        """
        return cls.query.filter_by(nominativo=nominativo).first()

    @classmethod
    def esiste_da_email(cls, email: str) -> "Utente | None":
        """
        Verifica l'esistenza di un utente data l'email.

        :param email: Email dell'utente
        :return: Utente se esiste, altrimenti None
        """
        return cls.query.filter_by(email=email).first()

    def punti_stagione(self, stagione: int) -> float:
        """
        Calcola il totale dei punti dell'utente in una stagione.

        :param stagione: Anno o identificativo della stagione
        :return: Somma dei punti ottenuti nella stagione (0 se assenti)
        """
        return db.session.scalar(
            db.select(func.coalesce(func.sum(Cronologia.modifica_punti), 0))
            .where(
                Cronologia.utente_id == self.id,
                Cronologia.stagione == stagione
            )
        )

    def elenco_cronologia_stagione(
        self,
        stagione: int,
        cronologicamente: bool = True
    ) -> list["Cronologia"]:
        """
        Restituisce la cronologia dell'utente per una determinata stagione.

        :param stagione: Anno o identificativo della stagione
        :param cronologicamente: Se True, ordina gli eventi per data
        :return: Lista di eventi di tipo Cronologia
        """
        cronologia = self.cronologia_studente.filter_by(
            stagione=stagione
        ).all()

        if cronologicamente:
            cronologia = sorted(
                cronologia,
                key=lambda evento: converti_a_unix(evento.data)
            )

        return cronologia

    @classmethod
    def elenco_utenti(cls) -> list["Utente"]:
        """
        Restituisce l'elenco di tutti gli utenti presenti nel sistema.

        :return: Lista di Utente
        """
        return cls.query.all()

    @classmethod
    def elenco_studenti(cls) -> list["Utente"]:
        """
        Restituisce l'elenco di tutti gli studenti (non admin).

        :return: Lista di Utente studenti
        """
        return cls.query.filter_by(admin_user=False).all()

    @classmethod
    def elenco_admin(cls) -> list["Utente"]:
        """
        Restituisce l'elenco di tutti gli utenti amministratori.

        :return: Lista di Utente admin
        """
        return cls.query.filter_by(admin_user=True).all()

    @classmethod
    def elenco_studenti_registrati(cls) -> list["Utente"]:
        """
        Restituisce l'elenco degli studenti con account attivo.

        :return: Lista di Utente studenti registrati
        """
        return cls.query.filter_by(
            admin_user=False,
            account_attivo=True
        ).all()

    @classmethod
    def elenco_studenti_non_registrati(cls) -> list["Utente"]:
        """
        Restituisce l'elenco degli studenti con account non attivo.

        :return: Lista di Utente studenti non registrati
        """
        return cls.query.filter_by(
            admin_user=False,
            account_attivo=False
        ).all()
