import werkzeug
from werkzeug.security import generate_password_hash

from ..modelli import User
from ..errors_utils import FailedSignUpError
from werkzeug.security import check_password_hash
from flask_login import login_user
from sito.errors_utils import FailedLoginError

from .. import db, app

with app.app_context():
    import sito.database_funcs as db_funcs


def login(email: str, password: str) -> None:
    """
    data un email ed una password fa il login di un account
    """
    user = db_funcs.user_da_email(email)
    if not user:
        raise FailedLoginError("Questo utente non esiste")
    if not user.account_attivo:
        raise FailedLoginError("Questo account non è attivo")
    if not check_password_hash(user.password, password):
        raise FailedLoginError("La password inserita non è corretta")
    login_user(user, remember=True)


def crea_user(**kwargs) -> None:
    """
    dato i parametri:
    -email
    -nominativo
    -squadra
    -password
    -account_attivo (facoltativo)
    -admin user (facoltativo)
    -nome della classe
    crea un utente
    """
    user = db_funcs.user_da_email(kwargs["email"]) or db_funcs.user_da_nominativo(
        kwargs["nominativo"]
    )
    if user:
        raise FailedSignUpError("Questo utente esiste già")
    nuovo_utente = User(
        email=kwargs["email"],
        nominativo=kwargs["nominativo"],
        squadra=kwargs["squadra"],
        password=generate_password_hash(kwargs["password"], method="pbkdf2:sha256"),
        punti="0.0",
        account_attivo=kwargs.get("account_attivo", 0),
        admin_user=kwargs.get("admin_user", 0),
        squadra_id=db_funcs.squadra_da_nome(kwargs["squadra"]).id,
        classe_id=db_funcs.classe_da_nome(kwargs["classe_name"]).id,
    )
    db.session.add(nuovo_utente)
    db.session.commit()


def crea_admin_user(**kwargs) -> None:
    """
    wrapper della funzione crea user per gli admin :
    prende i parametri :
    -email
    -nominativo
    -password
    """
    kwargs["admin_user"] = 1
    kwargs["classe_name"] = "admin"
    kwargs["squadra"] = "admin"
    kwargs["account_attivo"] = 1
    crea_user(**kwargs)
