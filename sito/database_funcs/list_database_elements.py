from sito.database_funcs.database_queries import studenti_da_classe
from ..modelli import User, Classi, Info
from .database_queries import studenti_da_classe


def elenco_utenti() -> list[User]:
    return User.query.filter_by().all()


def elenco_studenti() -> list[User]:

    return [utente for utente in User.query.filter_by().all() if not utente.admin_user]


def elenco_admin() -> list[User]:
    return [utente for utente in User.query.filter_by().all() if utente.admin_user]


def elenco_studenti_registrati() -> list[User]:
    return [studente for studente in elenco_studenti() if studente.account_attivo]


def elenco_user_da_classe_id_e_nome_squadra(
    classe_id: int, nome_squadra: str
) -> list[User]:

    return User.query.filter_by(classe_id=classe_id, squadra=nome_squadra).all()


def elenco_tutte_le_classi() -> list[Classi]:
    return Classi.query.filter_by().all()


def elenco_classi_studenti() -> list[Classi]:
    return [classe for classe in elenco_tutte_le_classi() if classe.classe != "admin"]


def elenco_squadre_da_classe(classe: Classi) -> set[str]:
    return {studente.squadra for studente in studenti_da_classe(classe)}


def get_last_season() -> int:
    return Info.query.filter_by().first().last_season
