from sito.modelli import Cronologia, User
from .. import db


def elimina_evento_cronologia(evento: Cronologia) -> None:
    db.session.delete(evento)


def cronologia_utente(utente: User, stagione: int) -> list[Cronologia]:
    eventi = utente.cronologia_studente
    return [evento for evento in eventi if evento.stagione == stagione]
