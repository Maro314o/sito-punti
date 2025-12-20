from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

from ..modelli import Utente, Squadra, Classe
from ..errors_utils import FailedSignUpError
from sito.errors_utils import FailedLoginError
from .. import db


def login(email: str, password: str) -> None:
    """
    Esegue il login di un utente dato email e password.

    Verifica che l'utente esista, che l'account sia attivo
    e che la password sia corretta. Se tutte le condizioni
    sono soddisfatte, esegue il login con Flask-Login.

    Args:
        email (str): Email dell'utente.
        password (str): Password in chiaro dell'utente.

    Raises:
        FailedLoginError: Se l'utente non esiste, l'account non è attivo
                          o la password è errata.
    """
    user = Utente.query.filter_by(email=email).first()
    if not user:
        raise FailedLoginError("Questo utente non esiste")
    if not user.account_attivo:
        raise FailedLoginError("Questo account non è attivo")
    if not check_password_hash(user.password, password):
        raise FailedLoginError("La password inserita non è corretta")

    login_user(user, remember=True)


def crea_user(**kwargs) -> None:
    """
    Crea un nuovo utente nel database.

    Richiede i parametri:
        - email (str)
        - nominativo (str)
        - squadra (str)
        - password (str)
        - classe_name (str)

    Parametri opzionali:
        - account_attivo (int): 0 o 1, default 0
        - admin_user (int): 0 o 1, default 0

    Args:
        **kwargs: Dizionario con i parametri richiesti e opzionali.

    Raises:
        FailedSignUpError: Se un utente con la stessa email o nominativo esiste già.
    """
    if Utente.esiste_da_email(kwargs["email"]) or Utente.esiste_da_nominativo(kwargs["nominativo"]):
        raise FailedSignUpError("Questo utente esiste già")

    nuovo_utente = Utente(
        email=kwargs["email"],
        nominativo=kwargs["nominativo"],
        squadra=kwargs["squadra"],
        password=generate_password_hash(kwargs["password"], method="pbkdf2:sha256"),
        account_attivo=kwargs.get("account_attivo", 0),
        admin_user=kwargs.get("admin_user", 0),
        squadra_id=Squadra.da_nome(kwargs["squadra"]).id,
        classe_id=Classe.da_nome(kwargs["classe_name"]).id,
    )

    db.session.add(nuovo_utente)
    db.session.commit()


def crea_admin_user(**kwargs) -> None:
    """
    Wrapper della funzione `crea_user` per creare un amministratore.

    Imposta automaticamente:
        - admin_user = 1
        - classe_name = "admin"
        - squadra = "admin"
        - account_attivo = 1

    Args:
        **kwargs: Dizionario con i parametri richiesti:
                  - email (str)
                  - nominativo (str)
                  - password (str)
    """
    kwargs["admin_user"] = 1
    kwargs["classe_name"] = "admin"
    kwargs["squadra"] = "admin"
    kwargs["account_attivo"] = 1
    crea_user(**kwargs)
