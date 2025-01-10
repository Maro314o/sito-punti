from typing import Optional, List
from ..modelli import Squadra, User, Classi


def user_da_nominativo(nominativo: str) -> Optional[User]:
    """
    Restituisce un oggetto utente dato il suo nominativo.
    """
    return User.query.filter_by(nominativo=nominativo).first()


def user_da_id(id: int) -> Optional[User]:
    """
    Restituisce un oggetto utente dato il suo id.
    """
    return User.query.filter_by(id=id).first()


def user_da_email(email: str) -> Optional[User]:
    """
    Restituisce un oggetto utente dato la sua email.
    """
    return User.query.filter_by(email=email).first()


def studenti_da_classe(classe: Classi) -> List[User]:
    """
    Restituisce gli studenti di una classe.
    """
    return classe.studenti


def classe_da_nome(classe_name: str) -> Optional[Classi]:
    """
    Restituisce un oggetto classe dato il suo nome.
    """
    return Classi.query.filter_by(classe=classe_name).first()


def classe_da_id(classe_id: int) -> Optional[Classi]:
    """
    Restituisce un oggetto classe dato il suo id.
    """
    return Classi.query.filter_by(id=classe_id).first()


def squadre_da_classe(classe: Classi) -> List[Squadra]:
    """
    Restituisce le squadre di una classe.
    """
    return classe.squadre


def squadra_da_nome(nome_squadra: str) -> Optional[Squadra]:
    """
    Restituisce un oggetto squadra dato il suo nome.
    """
    return Squadra.query.filter_by(nome_squadra=nome_squadra).first()


def squadra_da_id(squadra_id: int) -> Optional[Squadra]:
    """
    Restituisce un oggetto squadra dato il suo id.
    """
    return Squadra.query.filter_by(id=squadra_id).first()
