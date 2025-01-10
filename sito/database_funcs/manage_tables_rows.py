import sqlalchemy
from ..modelli import Classi, Squadra
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

    db.session.commit()


def crea_squadra(**kwargs):
    """
    dato i parametri:
    nome_squadra
    numero_componenti
    punti_reali
    punti_compensati
    classe_name
    crea una squadra
    """
    squadra = db_funcs.squadra_da_nome(kwargs["nome_squadra"])
    if squadra:
        raise ValueError(
            "questa squadra esiste gia'"
        )  # TODO : implementare l'errore corretto per questo caso
    nuova_squadra = Squadra(
        nome_squadra=kwargs["nome_squadra"],
        numero_componenti=int(kwargs.get("numero_componenti", 0)),
        punti_reali=kwargs.get("punti_reali", "0.0"),
        punti_compensati=kwargs.get("punti_compensati", "0.0"),
        classe_id=db_funcs.classe_da_nome(kwargs["classe_name"]).id,
    )
    db.session.add(nuova_squadra)
    db.session.commit()
