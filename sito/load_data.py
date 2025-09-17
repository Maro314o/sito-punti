import pandas as pd
from pathlib import Path
from os import path
import os
import datetime

import sito.database_funcs.point_funcs.modify_points_utils as modfiy_point_utils

from .modelli import User
import sito.misc_utils_funcs as mc_utils

from . import db

import sito.database_funcs as db_funcs
import sito.excel_funcs.load_excel_helpers as load_excel_helpers


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
GLOBAL_DATA = path.join(Path.cwd(), "data", "global_data.json")

NAME_FILE_MERGED = path.join(Path.cwd(), "data", "foglio.xlsx")


def load_data(current_user: User) -> None:
    """
    processa il file excel caricato
    """
    errori = 0
    file = pd.read_excel(NAME_FILE_MERGED, sheet_name=None)
    load_excel_helpers.reset_database()
    errori += load_excel_helpers.genera_struttura_classi(file)
    errori += load_excel_helpers.processa_dati_dataframe(file)

    studenti = db_funcs.elenco_studenti()
    squadre = db_funcs.elenco_squadre_studenti()
    classi_studenti = db_funcs.elenco_classi_studenti()
    for studente in studenti:
        db_funcs.aggiorna_punti_cumulativi_eventi(studente)
        db_funcs.aggiorna_punti(studente)
        db_funcs.aggiorna_punti_squadra(studente)
    for classe in classi_studenti:
        classe.massimo_studenti_squadra = (
            load_excel_helpers.numero_massimo_componenti_squadra_in_classe(classe)
        )

    for squadra in squadre:
        modfiy_point_utils.compensa_punti_squadra(squadra)
    db.session.commit()

    log_str = f"{datetime.datetime.now()} | {current_user.nominativo} ha appena caricato un file excel con {errori} errori\n"
    mc_utils.append_to_file(LOG_FILE, log_str)
    last_upload_time = str(datetime.datetime.now().date())
    mc_utils.set_item_of_json(GLOBAL_DATA, "ultimo_upload", last_upload_time)


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
    merged_df = merged_df.drop_duplicates()

    other_sheets = {
        sheet: pd.read_excel(NAME_FILE, sheet_name=sheet)
        for sheet in pd.ExcelFile(NAME_FILE).sheet_names
        if sheet != "Challenge"
    }

    with pd.ExcelWriter(NAME_FILE_MERGED) as writer:
        merged_df.to_excel(writer, sheet_name="Challenge", index=False)

        for sheet_name, df in other_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
