import sqlalchemy
from ..modelli import User
from werkzeug.security import generate_password_hash
from .. import db
from ..errors_utils import UserAlreadyExists
def crea_user(**kwargs) -> None:
    try:
        nuovo_utente = User(
            email=kwargs["email"],
            nominativo=kwargs["nominativo"],
            password=generate_password_hash(kwargs["passoword"], method="sha256"),
            punti="0",
            account_attivo=1,
            admin_user=kwargs.get("admin_user", 0),
            classe_id=db_funcs.classe_da_nome(kwargs["classe_name"]).id,
        )
        db.session.add(nuovo_utente)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise UserAlreadyExists(f"Un utente con questa email : {kwargs["email"]} o/e questo nominativo : {kwargs["nominativo"]} ")
