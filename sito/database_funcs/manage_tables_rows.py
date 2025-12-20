from ..modelli import Classe, Squadra
from .. import db
from ..errors_utils import ClasseAlreadyExistsError



def crea_classe(nome_classe:str):
    """
    dato un nome crea una classe
    """

    if Classe.esiste_da_nome(nome_classe):
        raise ClasseAlreadyExistsError("Esiste già una classe con questo nome")
    db.session.add(Classe(nome_classe=nome_classe))

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

    if Squadra.esiste_da_nome("nome_squadra"):
        raise ValueError(
            "questa squadra esiste gia'"
        )  # TODO : implementare l'errore corretto per questo caso
    nuova_squadra = Squadra(
        nome_squadra=kwargs["nome_squadra"],
        numero_componenti=int(kwargs.get("numero_componenti", 0)),
        classe_id=Classe.da_nome(kwargs["classe_name"]).id,
    )
    db.session.add(nuova_squadra)
    db.session.commit()
