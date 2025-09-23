from typing import Dict, Tuple


from sito.database_funcs import list_database_elements
from sito.database_funcs.manage_tables_rows import crea_squadra
from .. import db
from ..modelli import Cronologia, Info, Classi, Squadra, User
import sito.database_funcs as db_funcs
import sito.misc_utils_funcs as mc_utils
from pathlib import Path
from os import path
import pandas as pd
import math
import sito.database_funcs.database_queries as db_queries
import datetime
import sito.auth_funcs as auth_utils

ERROR_FILE = path.join(Path.cwd(), "data", "errore.txt")
NAME_FILE_MERGED = path.join(Path.cwd(), "data", "foglio.xlsx")
ERROR = True
NO_ERROR = False


def elimina_studenti_non_presenti(nominativi_trovati: set[str]) -> None:
    """
    elimina tutti gli studenti che non fanno parte della lista degli studenti passati nel file excel
    """
    for utente in db_funcs.elenco_studenti():
        if utente.nominativo not in nominativi_trovati:
            db.session.delete(utente)


def riga_nulla(riga: list[str]) -> bool:
    """
    controlla se la riga che stiamo analizzando e' nulla (quindi composta da valori nan)
    """

    return all(str(valore).lower() in ("nan","nat") for valore in riga)


def reset_database() -> None:
    """
    prepara il database per uno stato di scrittura via il caricamento di un file excel
    """
    db.session.query(Cronologia).delete()
    db.session.query(Info).delete()
    User.query.filter_by(account_attivo=0).delete()
    db.session.query(Classi).delete()
    db.session.query(Squadra).delete()
    db_funcs.crea_classe("admin")
    db_funcs.crea_classe("Nessuna_squadra")
    db_funcs.crea_squadra(nome_squadra="admin", classe_name="admin")
    db_funcs.crea_squadra(nome_squadra="Nessuna_squadra", classe_name="Nessuna_squadra")

    mc_utils.clear_file(ERROR_FILE)

    db.session.commit()


def processa_riga_classe(numero_riga: int, riga: list[str], nome_classe: str) -> str:
    # la riga dovrebbe essere [nominativo,squadra]
    squadra = "Nessuna_squadra"
    nominativo = mc_utils.capitalize_all(riga[0])
    if type(riga[1])is not float:
        squadra = riga[1]
        oggetto_squadra = db_queries.squadra_da_nome(squadra)
        if not oggetto_squadra:
            crea_squadra(
                nome_squadra=squadra, numero_componenti=1, classe_name=nome_classe
            )
        else:
            oggetto_squadra.numero_componenti += 1

    else:
        nome_classe = squadra
        error_str = f"{datetime.datetime.now()} | errore alla linea {numero_riga} del foglio {nome_classe} del database : La cella della squadra per questo utente ({nominativo}) e' vuota.Gli verra' assegnata una squadra provvisoria chiamata \"Nessuna_squadra\"\n"

        mc_utils.append_to_file(ERROR_FILE, error_str)

    utente = db_queries.user_da_nominativo(nominativo)
    if utente:
        utente.nominativo = nominativo
        utente.squadra = squadra
        utente.punti = "0.0"
        utente.classe_id = db_funcs.classe_da_nome(nome_classe).id
        utente.squadra_id = db_funcs.squadra_da_nome(squadra).id

    else:
        auth_utils.crea_user(
            email=f"email_non_registrata_per_{mc_utils.insert_underscore_name(nominativo)}",
            nominativo=nominativo,
            squadra=squadra,
            password="",
            account_attivo=0,
            classe_name=nome_classe,
        )
    return nominativo


def genera_studenti_e_squadre(
    classe_dataframe: pd.DataFrame, nome_classe: str
) -> set[str]:
    """
    genera tutti gli studenti e squadre di una determinata classe
    """

    nominativi_trovati = set()
    for numero_riga, riga in enumerate(classe_dataframe.values.tolist()):
        # la funzione principale della funzione processa_riga_classe non e' ritornare la stringa ma e' una cosa in piu' che fa'
        nominativo = processa_riga_classe(numero_riga, riga, nome_classe)
        nominativi_trovati.add(nominativo)
    return nominativi_trovati


def genera_struttura_classi(file_sheets: Dict[str, pd.DataFrame]) -> int:
    """
    genera le classi caricate e gli studenti di quelle classi nel database per poterli successivamente scrivere
    """
    _, *lista_fogli_classi = file_sheets.keys()
    nominativi_trovati = set()

    for nome_classe in lista_fogli_classi:
        db_funcs.crea_classe(nome_classe)
        nominativi_trovati |= genera_studenti_e_squadre(
            file_sheets[nome_classe], nome_classe
        )

    elimina_studenti_non_presenti(nominativi_trovati)
    db.session.commit()
    return 0  # TODO implementare conteggio degli errori in questa funzione (probabilmente non prima dell'update generale degli errori)


def processa_riga_dataset(
    numero_riga: int, riga: list
) -> Tuple[int, bool]:  # ritornare la stagione serve per verificare la stagione massima
    """
    processa una singola riga della pagina del dataset (foglio che contiene i punti)
    ritorno anche la stagione e se c'e' stato un errore
    """
    # riga dovrebbe seguire questo formato [data,stagione,classe,alunno,attivita',punti]
    # 0 data
    # 1 stagione
    # 2 classe
    # 3 alunno
    # 4 attivita'
    # 5 punti
    if riga_nulla(riga):
        error_str = f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : La riga corrente e' vuota\n"
        mc_utils.append_to_file(ERROR_FILE, error_str)
        return 0, ERROR
    data, _ = str(
        riga[0]
    ).split()  # la seconda parte dello split dovrebbe essere l'ora,che non e' usata e solitamente e' 00:00:00
    stagione: int = riga[1]
    nome_classe: str = riga[2]
    nominativo: str = mc_utils.capitalize_all(riga[3])
    attivita: str = riga[4]
    punti: float = riga[5]
    if not db_funcs.user_da_nominativo(nominativo):
        error_str = f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : non è stato possibile modificare i punti dell' utente {nominativo} della classe {nome_classe}. Controlla se ci sono errori nella scrittura del suo nome o se non è stato aggiunto ad una classe nel corrispettivo foglio .xlsx\n"
        mc_utils.append_to_file(ERROR_FILE, error_str)
        return stagione, ERROR

    db.session.add(
        Cronologia(
            data=data,
            stagione=stagione,
            attivita=attivita,
            modifica_punti=punti,
            punti_cumulativi=0.0,
            utente_id=db_funcs.user_da_nominativo(nominativo).id,
        )
    )
    return stagione, NO_ERROR


def processa_dati_dataframe(file_sheets: Dict[str, pd.DataFrame]) -> int:
    """
    processa tutti i dati e punti del dataset
    """

    dataset, *_ = file_sheets.keys()
    last_season = 0
    errori = 0
    for numero_riga, riga in enumerate(file_sheets[dataset].values.tolist()):
        stagione, errore = processa_riga_dataset(numero_riga, riga)
        last_season = stagione if stagione > last_season else last_season
        errori += errore
    db.session.query(Info).delete()
    db.session.add(Info(last_season=last_season))
    db.session.commit()
    return errori


def numero_massimo_componenti_squadra_in_classe(classe: Classi) -> int:
    componenti_massimi = 0
    for squadra in list_database_elements.elenco_squadre_da_classe(classe):
        if squadra.numero_componenti > componenti_massimi:
            componenti_massimi = squadra.numero_componenti
    return componenti_massimi
