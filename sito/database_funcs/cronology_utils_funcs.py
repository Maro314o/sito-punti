from sito.modelli import Cronologia, User
from .. import db
from ..misc_utils_funcs import converti_a_unix


def ordina_cronologicamente(lista_cronologia: list[Cronologia]) -> list[Cronologia]:
    """
    ordina gli eventi di una cronologia in ordine cronologico
    """
    return sorted(lista_cronologia, key=lambda evento: converti_a_unix(evento.data))


def elimina_evento_cronologia(evento: Cronologia) -> None:
    """
    elimina un oggetto evento
    """
    db.session.delete(evento)


def cronologia_user(utente: User) -> list[Cronologia]:
    """
    restituisce l'intera cronologia di un utente ordinata cronolicamente
    """

    return sorted(
        ordina_cronologicamente(utente.cronologia_studente),
        key=lambda evento: evento.stagione,
    )


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
