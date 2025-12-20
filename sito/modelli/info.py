from .. import db


class Info(db.Model):
    """
    Modello ORM che rappresenta informazioni globali dell'applicazione.

    È pensato come singleton per memorizzare dati condivisi come
    l'ultima stagione disponibile.
    """

    id = db.Column(db.Integer, primary_key=True)
    ultima_stagione = db.Column(db.Integer)

    @classmethod
    def _get_singleton(cls) -> "Info":
        """
        Restituisce l'unica istanza di Info, creandola se necessario.

        Returns:
            Info: Istanza singleton.
        """
        info = cls.query.first()
        if info is None:
            info = cls(ultima_stagione=1)
            db.session.add(info)
            db.session.commit()
        return info

    @classmethod
    def ottieni_ultima_stagione(cls) -> int:
        """
        Restituisce l'ultima stagione registrata.

        Returns:
            int: Ultima stagione.
        """
        return cls._get_singleton().ultima_stagione

    @classmethod
    def modifica_ultima_stagione(cls, stagione: int) -> None:
        """
        Aggiorna il valore dell'ultima stagione.

        Args:
            stagione (int): Nuovo valore della stagione.
        """
        info = cls._get_singleton()
        info.ultima_stagione = stagione
        db.session.commit()
