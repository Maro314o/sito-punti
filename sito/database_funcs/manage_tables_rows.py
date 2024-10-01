import sqlalchemy
from ..modelli import Classi
from .. import db, app
from ..errors_utils import ClasseAlreadyExistsError

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
