from typing import List
from ..modelli import Squadra, User, Classi, Info

NOT_AVALIDABLE = ["admin", "Nessuna_squadra"]



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


