import json
import pandas as pd
from pathlib import Path
from os import path
import os
import datetime

from .modelli import User
from sito.database_funcs.database_queries import user_da_nominativo
import sito.misc_utils_funcs as mc_utils

from . import db

from .modelli import User, Classi, Cronologia, Info
import sito.database_funcs as db_funcs
import sito.auth_funcs as auth_utils


mesi = {
    "gennaio": 1,
    "febbraio": 2,
    "marzo": 3,
    "aprile": 4,
    "maggio": 5,
    "giugno": 6,
    "luglio": 7,
    "agosto": 8,
    "settembre": 9,
    "ottobre": 10,
    "novembre": 11,
    "dicembre": 12,
}
ERROR_FILE = path.join(Path.cwd(), "data", "errore.txt")
LOG_FILE = path.join(Path.cwd(), "data", "log.txt")
NAME_FILE = path.join(Path.cwd(), "data", "foglio_pre-merge.xlsx")
FILE_ERRORE = path.join(Path.cwd(), "data", "errore.txt")
GLOBAL_DATA = path.join(Path.cwd(), "data", "global_data.json")
NAME_FILE_MERGED = path.join(Path.cwd(), "data", "foglio.xlsx")


def load_data(current_user: User) -> None:
    db.session.query(Cronologia).delete()
    db.session.query(Info).delete()
    User.query.filter_by(account_attivo=0).delete()
    db.session.query(Classi).delete()
    db_funcs.crea_classe("admin")
    db.session.commit()

    file = pd.read_excel(NAME_FILE_MERGED, sheet_name=None)
    dataset, *lista_fogli = file.keys()
    nominativi_trovati = set()

    mc_utils.clear_file(FILE_ERRORE)
    for classe_name in lista_fogli:
        db_funcs.crea_classe(classe_name)
        for numero_riga, riga in enumerate(file[classe_name].values.tolist()):
            nominativo = riga[0]
            nominativo = mc_utils.capitalize_all(nominativo)
            nominativi_trovati.add(nominativo)
            utente = user_da_nominativo(nominativo)
            if len(riga) == 1:

                with open(ERROR_FILE, "a") as f:
                    f.write(
                        f"{datetime.datetime.now()} | errore alla linea {numero_riga} del foglio {classe_name} del edatabase : La cella della squadra per questo utente e' vuota.Gli verra' assegnata una squadra provvisoria chiamata \"Nessuna_squadra\"\n"
                    )
                squadra = "Nessuna_squadra"
            else:
                squadra = riga[1]
            if not utente:
                auth_utils.crea_user(
                    email=f"email_non_registrata_per_{mc_utils.insert_underscore_name(nominativo)}",
                    nominativo=nominativo,
                    squadra=squadra,
                    password="",
                    account_attivo=0,
                    classe_name=classe_name,
                )
            else:
                utente.nominativo = nominativo
                utente.squadra = squadra
                utente.punti = "0"
                utente.classe_id = db_funcs.classe_da_nome(classe_name).id

    db.session.commit()
    last_season = 0
    errori = 0
    for numero_riga, riga in enumerate(file[dataset].values.tolist()):
        # 0 data
        # 1 stagione
        # 2 classe
        # 3 alunno
        # 4 attivita'
        # 5 punti
        print(str(riga[0]).split())
        data, _ = str(riga[0]).split()
        stagione = riga[1]
        classe_name = riga[2]
        nominativo = mc_utils.capitalize_all(riga[3])

        attivita = riga[4]
        punti = riga[5]
        if all(str(valore).lower() == "nan" for valore in riga):
            with open(ERROR_FILE, "a") as f:
                f.write(
                    f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : La riga corrente e' vuota\n"
                )
            errori += 1
            continue
        elif not db_funcs.user_da_nominativo(nominativo):

            print(nominativo)
            with open(ERROR_FILE, "a") as f:
                f.write(
                    f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : non è stato possibile modificare i punti dell' utente {nominativo} della classe {classe_name}. Controlla se ci sono errori nella scrittura del suo nome o se non è stato aggiunto ad una classe nel corrispettivo foglio .xlsx\n"
                )
            errori += 1
            continue

        last_season = stagione if stagione > last_season else last_season
        db.session.add(
            Cronologia(
                data=data,
                stagione=stagione,
                attivita=attivita,
                modifica_punti=punti,
                punti_cumulativi=0,
                utente_id=db_funcs.user_da_nominativo(nominativo).id,
            )
        )
    db.session.query(Info).delete()
    db.session.add(Info(last_season=last_season))
    db.session.commit()
    for utente in db_funcs.elenco_studenti():
        if utente.nominativo not in nominativi_trovati:
            db.session.delete(utente)
    db.session.commit()
    studenti = db_funcs.elenco_studenti()
    for studente in studenti:
        db_funcs.aggiorna_punti_cumulativi(studente)
        db_funcs.aggiorna_punti(studente)
    with open(LOG_FILE, "a") as f:
        f.write(
            f"{datetime.datetime.now()} | {current_user.nominativo} ha appena caricato un file excel con {errori} errori\n"
        )
    with open(GLOBAL_DATA, "r") as file:
        global_data = json.load(file)
    global_data["ultimo_upload"] = str(datetime.datetime.now().date())
    with open(GLOBAL_DATA, "w") as file:
        json.dump(global_data, file, indent=4)


def merge_excel() -> None:
    """
    fa il merge di due file excel
    """

    if not os.path.exists(NAME_FILE_MERGED):
        os.rename(NAME_FILE, NAME_FILE_MERGED)
        return
    df1 = pd.read_excel(NAME_FILE)
    df2 = pd.read_excel(NAME_FILE_MERGED)
    merged_df = pd.concat([df1, df2], ignore_index=True)
    merged_df.to_excel("merged_file.xlsx", index=False)
    merged_df = merged_df.drop_duplicates()

    other_sheets = {
        sheet: pd.read_excel(NAME_FILE_MERGED, sheet_name=sheet)
        for sheet in pd.ExcelFile(NAME_FILE_MERGED).sheet_names
        if sheet != "Challenge"
    }

    with pd.ExcelWriter(NAME_FILE_MERGED) as writer:
        merged_df.to_excel(writer, sheet_name="Challenge", index=False)

        for sheet_name, df in other_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
