import sqlalchemy
from ..modelli import User, Classi
from werkzeug.security import generate_password_hash
from .. import db, app
from ..errors_utils import UserAlreadyExistsError, ClasseAlreadyExistsError

with app.app_context():
    import sito.database_funcs as db_funcs


def crea_classe(classe_name):
    """
    dato un nome crea una classe
    """
    try:
        db.session.add(Classi(classe=classe_name))
    except sqlalchemy.exc.IntegrityError:
        raise ClasseAlreadyExistsError("Esiste già una classe con questo nome")


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
    """
    try:
        nuovo_utente = User(
            email=kwargs["email"],
            nominativo=kwargs["nominativo"],
            squadra=kwargs["squadra"],
            password=generate_password_hash(kwargs["password"], method="sha256"),
            punti="0",
            account_attivo=kwargs.get("account_attivo", 0),
            admin_user=kwargs.get("admin_user", 0),
            classe_id=db_funcs.classe_da_nome(kwargs["classe_name"]).id,
        )
        db.session.add(nuovo_utente)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise UserAlreadyExistsError(
            f"Un utente con questa email : {kwargs['email']} o/e questo nominativo : {kwargs['nominativo']} "
        )


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
