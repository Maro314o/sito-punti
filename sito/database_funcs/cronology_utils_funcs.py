from sito.modelli import Cronologia, User
from .. import db


def elimina_evento_cronologia(evento: Cronologia) -> None:
    """
    elimina un oggetto evento
    """
    db.session.delete(evento)


def cronologia_user(utente: User) -> list[Cronologia]:
    """
    restituisce l'intera cronologia di un utente
    """
    return utente.cronologia_studente


def cronologia_user_di_una_stagione(utente: User, stagione: int) -> list[Cronologia]:
    """
    restituisce tutta la cronologia di un utente di una determinata stagione
    """
    eventi = cronologia_user(utente)
    return [evento for evento in eventi if evento.stagione == stagione]


def evento_da_id(id: int) -> Cronologia | None:
    """
    restituisce un oggetto evento da un id
    """
    return Cronologia.query.filter_by(id=id).first()
