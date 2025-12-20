from sito.misc_utils_funcs.parse_utils import converti_a_unix
from sito.modelli.cronologia import Cronologia
from .. import db
from sqlalchemy import func
from flask_login import UserMixin


class Utente(db.Model, UserMixin):
    """Modello ORM che rappresenta un utente del sistema.

    Può essere uno studente o un amministratore e contiene informazioni
    anagrafiche, di autenticazione e relazioni con la cronologia delle attività.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nominativo = db.Column(db.String(150), unique=True)
    squadra = db.Column(db.String(150))
    password = db.Column(db.String(150))
    admin_user = db.Column(db.Integer)
    account_attivo = db.Column(db.Integer)

    cronologia_studente = db.relationship("Cronologia", lazy="dynamic")

    classe_id = db.Column(db.Integer, db.ForeignKey("classe.id"))
    squadra_id = db.Column(db.Integer, db.ForeignKey("squadra.id"))

    @classmethod
    def da_id(cls, id: int) -> "Utente":
        """Restituisce un utente dato il suo ID.

        Args:
            id (int): ID dell'utente.

        Returns:
            Utente: Istanza dell'utente corrispondente.

        Raises:
            sqlalchemy.exc.NoResultFound: Se l'utente non esiste.
        """
        return cls.query.filter_by(id=id).one()

    @classmethod
    def da_nominativo(cls, nominativo: str) -> "Utente":
        """Restituisce un utente dato il suo nominativo.

        Args:
            nominativo (str): Nome completo dell'utente.

        Returns:
            Utente: Istanza dell'utente corrispondente.

        Raises:
            sqlalchemy.exc.NoResultFound: Se l'utente non esiste.
        """
        return cls.query.filter_by(nominativo=nominativo).one()

    @classmethod
    def da_email(cls, email: str) -> "Utente":
        """Restituisce un utente dato l'email.

        Args:
            email (str): Email dell'utente.

        Returns:
            Utente: Istanza dell'utente corrispondente.

        Raises:
            sqlalchemy.exc.NoResultFound: Se l'utente non esiste.
        """
        return cls.query.filter_by(email=email).one()

    @classmethod
    def esiste_da_id(cls, id: int) -> "Utente | None":
        """Verifica se esiste un utente dato l'ID.

        Args:
            id (int): ID dell'utente.

        Returns:
            Utente | None: Utente se esiste, altrimenti None.
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def esiste_da_nominativo(cls, nominativo: str) -> "Utente | None":
        """Verifica se esiste un utente dato il nominativo.

        Args:
            nominativo (str): Nome completo dell'utente.

        Returns:
            Utente | None: Utente se esiste, altrimenti None.
        """
        return cls.query.filter_by(nominativo=nominativo).first()

    @classmethod
    def esiste_da_email(cls, email: str) -> "Utente | None":
        """Verifica se esiste un utente dato l'email.

        Args:
            email (str): Email dell'utente.

        Returns:
            Utente | None: Utente se esiste, altrimenti None.
        """
        return cls.query.filter_by(email=email).first()

    def punti_stagione(self, stagione: int) -> float:
        """Calcola il totale dei punti dell'utente in una stagione.

        Args:
            stagione (int): Anno o identificativo della stagione.

        Returns:
            float: Somma dei punti ottenuti nella stagione.
        """
        return db.session.scalar(
            db.select(func.coalesce(func.sum(Cronologia.modifica_punti), 0))
            .where(Cronologia.utente_id == self.id, Cronologia.stagione == stagione)
        )

    def elenco_cronologia_stagione(
        self, stagione: int, cronologicamente: bool = True
    ) -> list["Cronologia"]:
        """Restituisce la cronologia dell'utente per una stagione specifica.

        Args:
            stagione (int): Anno o identificativo della stagione.
            cronologicamente (bool, optional): Ordina gli eventi per data se True. Defaults to True.

        Returns:
            list[Chronologia]: Lista degli eventi dell'utente nella stagione.
        """
        cronologia = self.cronologia_studente.filter_by(stagione=stagione).all()

        if cronologicamente:
            cronologia = sorted(
                cronologia, key=lambda evento: converti_a_unix(evento.data)
            )

        return cronologia

    @classmethod
    def elenco_utenti(cls) -> list["Utente"]:
        """Restituisce tutti gli utenti presenti nel sistema.

        Returns:
            list[Utente]: Lista di tutti gli utenti.
        """
        return cls.query.all()

    @classmethod
    def elenco_studenti(cls) -> list["Utente"]:
        """Restituisce tutti gli studenti (non admin).

        Returns:
            list[Utente]: Lista degli utenti studenti.
        """
        return cls.query.filter_by(admin_user=False).all()

    @classmethod
    def elenco_admin(cls) -> list["Utente"]:
        """Restituisce tutti gli amministratori.

        Returns:
            list[Utente]: Lista degli utenti amministratori.
        """
        return cls.query.filter_by(admin_user=True).all()

    @classmethod
    def elenco_studenti_registrati(cls) -> list["Utente"]:
        """Restituisce gli studenti con account attivo.

        Returns:
            list[Utente]: Lista degli studenti registrati.
        """
        return cls.query.filter_by(admin_user=False, account_attivo=True).all()

    @classmethod
    def elenco_studenti_non_registrati(cls) -> list["Utente"]:
        """Restituisce gli studenti con account non attivo.

        Returns:
            list[Utente]: Lista degli studenti non registrati.
        """
        return cls.query.filter_by(admin_user=False, account_attivo=False).all()
