import sito.database_funcs as db_funcs
from ..modelli import User, Classi, Info


def elenco_utenti() -> list[User]:
    """
    restituisce l'elenco di tutti gli utenti
    """
    return User.query.filter_by().all()


def elenco_studenti() -> list[User]:
    """
    restituisce l'elenco di tutti gli studenti
    """
    return [utente for utente in User.query.filter_by().all() if not utente.admin_user]


def elenco_admin() -> list[User]:
    """
    restituisce l'elenco di tutti gli admin
    """
    return [utente for utente in User.query.filter_by().all() if utente.admin_user]


def elenco_studenti_registrati() -> list[User]:
    """
    restituisce l'elenco di tutti gli studenti registrati
    """
    return [studente for studente in elenco_studenti() if studente.account_attivo]


def elenco_user_da_classe_id_e_nome_squadra(
    classe_id: int, nome_squadra: str
) -> list[User]:
    """
    restituisce l'elenco di tutti gli studenti di una squadra di una classe
    """
    return User.query.filter_by(classe_id=classe_id, squadra=nome_squadra).all()


def elenco_tutte_le_classi() -> list[Classi]:
    """
    restituisce l'elenco di tutte le classi
    """
    return Classi.query.filter_by().all()


def elenco_classi_studenti() -> list[Classi]:
    """
    restituisce l'elenco di tutte le classi degli studenti (cioè tutte trannne quella admin)
    """
    return [classe for classe in elenco_tutte_le_classi() if classe.classe != "admin"]


def elenco_squadre_da_classe(classe: Classi) -> set[str]:
    """
    restituisce l'elenco di tutte le squadre di una classe
    """
    return {studente.squadra for studente in db_funcs.studenti_da_classe(classe)}


def get_last_season() -> int:
    """
    restituisce il numero della stagione più recente
    """
    return Info.query.filter_by().first().last_season
