import sqlalchemy
from ..modelli import User, Classi
from werkzeug.security import generate_password_hash
from .. import db, app
from ..errors_utils import UserAlreadyExists, ClasseAlreadyExists

with app.app_context():
    import sito.database_funcs as db_funcs


def crea_classe(classe_name):
    try:
        db.session.add(Classi(classe=classe_name))
    except sqlalchemy.exc.IntegrityError:
        raise ClasseAlreadyExists("Esiste già una classe con questo nome")


def crea_user(**kwargs) -> None:
    try:
        nuovo_utente = User(
            email=kwargs["email"],
            nominativo=kwargs["nominativo"],
            password=generate_password_hash(kwargs["password"], method="sha256"),
            punti="0",
            account_attivo=1,
            admin_user=kwargs.get("admin_user", 0),
            classe_id=db_funcs.classe_da_nome(kwargs["classe_name"]).id,
        )
        db.session.add(nuovo_utente)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise UserAlreadyExists(
            f"Un utente con questa email : {kwargs['email']} o/e questo nominativo : {kwargs['nominativo']} "
        )


def crea_admin_user(**kwargs) -> None:
    kwargs["admin_user"] = 1
    kwargs["classe_nome"] = "admin"
    crea_user(**kwargs)
