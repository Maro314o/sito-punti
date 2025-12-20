from sito.costanti import NOT_AVALIDABLE
from .. import db
from sqlalchemy import func


class Squadra(db.Model):
    """
    Modello ORM che rappresenta una squadra.

    Una squadra è composta da più studenti ed è associata a una classe.
    Il punteggio viene calcolato sommando i punti dei componenti.
    """

    id = db.Column(db.Integer, primary_key=True)
    nome_squadra = db.Column(db.String(150), unique=True)
    numero_componenti = db.Column(db.Integer)

    studenti_componenti = db.relationship("Utente", lazy="dynamic")

    classe_id = db.Column(db.Integer, db.ForeignKey("classe.id"))

    @classmethod
    def da_id(cls, id: int) -> "Squadra":
        """
        Restituisce una squadra dato l'ID.

        Args:
            id (int): ID della squadra.

        Returns:
            Squadra: Istanza della squadra.
        """
        return cls.query.filter_by(id=id).one()

    @classmethod
    def da_nome(cls, nome_squadra: str) -> "Squadra":
        """
        Restituisce una squadra dato il nome.

        Args:
            nome_squadra (str): Nome della squadra.

        Returns:
            Squadra: Istanza della squadra.
        """
        return cls.query.filter_by(nome_squadra=nome_squadra).one()

    @classmethod
    def esiste_da_id(cls, id: int) -> "Squadra | None":
        """
        Verifica l'esistenza di una squadra dato l'ID.

        Args:
            id (int): ID della squadra.

        Returns:
            Squadra | None: Squadra se esiste, altrimenti None.
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def esiste_da_nome(cls, nome_squadra: str) -> "Squadra | None":
        """
        Verifica l'esistenza di una squadra dato il nome.

        Args:
            nome_squadra (str): Nome della squadra.

        Returns:
            Squadra | None: Squadra se esiste, altrimenti None.
        """
        return cls.query.filter_by(nome_squadra=nome_squadra).first()

    def punti_stagione(self, stagione: int) -> float:
        """
        Calcola il punteggio totale della squadra in una stagione.

        Args:
            stagione (int): Identificativo della stagione.

        Returns:
            float: Punteggio totale compensato.
        """
        from .cronologia import Cronologia
        from .classe import Classe

        id_utenti_squadra = [
            studente.id for studente in self.studenti_componenti.all()
        ]

        punti_squadra = db.session.scalar(
            db.select(func.coalesce(func.sum(Cronologia.modifica_punti), 0))
            .where(
                Cronologia.utente_id.in_(id_utenti_squadra),
                Cronologia.stagione == stagione
            )
        )

        return punti_squadra * (
            Classe.da_id(self.classe_id).massimo_studenti_squadra
            / len(id_utenti_squadra)
        )
