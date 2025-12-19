from typing import Optional, List
from ..modelli import Squadra, User, Classi


def user_da_nominativo(nominativo: str) -> Optional[User]:
    """
    Restituisce un oggetto utente dato il suo nominativo.
    """
    return User.query.filter_by(nominativo=nominativo).first()




def user_da_email(email: str) -> Optional[User]:
    """
    Restituisce un oggetto utente dato la sua email.
    """
    return User.query.filter_by(email=email).first()










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
