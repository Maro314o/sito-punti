from typing import List
from ..modelli import Squadra, User, Classi, Info

NOT_AVALIDABLE = ["admin", "Nessuna_squadra"]


def elenco_utenti() -> List[User]:
    """
    Restituisce l'elenco di tutti gli utenti.
    """
    return User.query.all()


def elenco_studenti() -> List[User]:
    """
    Restituisce l'elenco di tutti gli studenti.
    """
    return User.query.filter_by(admin_user=False).all()


def elenco_admin() -> List[User]:
    """
    Restituisce l'elenco di tutti gli admin.
    """
    return User.query.filter_by(admin_user=True).all()


def elenco_studenti_registrati() -> List[User]:
    """
    Restituisce l'elenco di tutti gli studenti registrati.
    """
    return User.query.filter_by(admin_user=False, account_attivo=True).all()


def elenco_studenti_non_registrati() -> List[User]:
    """
    Restituisce l'elenco di tutti gli studenti non registrati.
    """
    return User.query.filter_by(admin_user=False, account_attivo=False).all()


def elenco_tutte_le_classi() -> List[Classi]:
    """
    Restituisce l'elenco di tutte le classi.
    """
    return Classi.query.all()


def elenco_tutte_le_squadre() -> List[Squadra]:
    """
    Restituisce l'elenco di tutte le squadre.
    """
    return Squadra.query.all()


def elenco_classi_studenti() -> List[Classi]:
    """
    Restituisce l'elenco di tutte le classi degli studenti (escludendo quelle in NOT_AVALIDABLE).
    """
    return Classi.query.filter(Classi.classe.notin_(NOT_AVALIDABLE)).all()


def elenco_squadre_studenti() -> List[Squadra]:
    """
    Restituisce l'elenco di tutte le squadre degli studenti (escludendo quelle in NOT_AVALIDABLE).
    """
    return Squadra.query.filter(Squadra.nome_squadra.notin_(NOT_AVALIDABLE)).all()


def elenco_studenti_da_classe(classe: Classi) -> List[User]:
    """
    Restituisce gli studenti di una classe.
    """
    return classe.studenti


def elenco_squadre_da_classe(classe: Classi) -> List[Squadra]:
    """
    Restituisce le squadre di una classe.
    """
    return classe.squadre


def get_last_season() -> int:
    """
    Restituisce il numero della stagione più recente.
    """
    info = Info.query.first()
    return info.last_season if info else 1
