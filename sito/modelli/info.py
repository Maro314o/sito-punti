

from .. import db
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ultima_stagione= db.Column(db.Integer)
    @classmethod
    def _get_singleton(cls) -> "Info":
        info = cls.query.first()
        if info is None:
            info = cls(ultima_stagione=1)
            db.session.add(info)
            db.session.commit()
        return info

    @classmethod
    def ottieni_ultima_stagione(cls) -> int:
        return cls._get_singleton().ultima_stagione

    @classmethod
    def modifica_ultima_stagione(cls, stagione: int) -> None:
        info = cls._get_singleton()
        info.ultima_stagione = stagione
        db.session.commit()

