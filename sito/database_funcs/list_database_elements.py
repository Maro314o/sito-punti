import sito.database_funcs as db_funcs
from ..modelli import Squadra, User, Classi, Info

NOT_AVALIDABLE = ["admin", "Nessuna_squadra"]


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


def elenco_tutte_le_classi() -> list[Classi]:
    """
    restituisce l'elenco di tutte le classi
    """
    return Classi.query.filter_by().all()


def elenco_tutte_le_squadre() -> list[Squadra]:
    """
    restituisce l'elenco di tutte le squadre
    """
    return Squadra.query.filter_by().all()


def elenco_classi_studenti() -> list[Classi]:
    """
    restituisce l'elenco di tutte le classi degli studenti (cioè tutte trannne quella admin)
    """
    return [
        classe
        for classe in elenco_tutte_le_classi()
        if classe.classe not in NOT_AVALIDABLE
    ]


def elenco_squadre_studenti() -> list[Squadra]:
    """
    restituisce l'elenco di tutte le squadre degli studenti (cioè tutte trannne quella admin)
    """
    return [
        squadra
        for squadra in elenco_tutte_le_squadre()
        if squadra.nome_squadra not in NOT_AVALIDABLE
    ]


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
