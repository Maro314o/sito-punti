from .. import db


class Cronologia(db.Model):
    """
    Modello ORM che rappresenta un evento di cronologia.

    Ogni evento descrive un'attività che modifica il punteggio
    di un utente in una determinata stagione.
    """

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(150))
    stagione = db.Column(db.Integer)
    attivita = db.Column(db.String(150))
    modifica_punti = db.Column(db.Float)

    utente_id = db.Column(db.Integer, db.ForeignKey("utente.id"))

    @classmethod
    def da_id(cls, id: int) -> "Cronologia":
        """
        Restituisce un evento di cronologia dato l'ID.

        Args:
            id (int): ID dell'evento.

        Returns:
            Cronologia: Istanza dell'evento.

        Raises:
            NoResultFound: Se l'evento non esiste.
        """
        return cls.query.filter_by(id=id).one()
