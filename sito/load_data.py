import pandas as pd
import os
import datetime

import sito.database_funcs.point_funcs.modify_points_utils as modfiy_point_utils

from .modelli import User
import sito.misc_utils_funcs as mc_utils

from . import db

import sito.database_funcs as db_funcs
import sito.excel_funcs.load_excel_helpers as load_excel_helpers
from sito.costanti import (
    EXCEL_MERGED_PATH,
    LOG_PATH,
    GLOBAL_DATA_PATH,
    EXCEL_PRE_MERGE_PATH,
)


def load_data(current_user: User) -> None:
    """
    processa il file excel caricato
    """
    errori = 0
    file = pd.read_excel(EXCEL_MERGED_PATH, sheet_name=None)
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
    mc_utils.append_to_file(LOG_PATH, log_str)
    last_upload_time = str(datetime.datetime.now().date())
    mc_utils.set_item_of_json(GLOBAL_DATA_PATH, "ultimo_upload", last_upload_time)


def merge_excel() -> None:
    """
    fa il merge di due file excel
    """

    if not os.path.exists(EXCEL_MERGED_PATH):
        os.rename(EXCEL_PRE_MERGE_PATH, EXCEL_MERGED_PATH)
        return
    df1 = pd.read_excel(EXCEL_PRE_MERGE_PATH)
    df2 = pd.read_excel(EXCEL_MERGED_PATH)
    merged_df = pd.concat([df1, df2], ignore_index=True)
    merged_df = merged_df.drop_duplicates()

    other_sheets = {
        sheet: pd.read_excel(EXCEL_PRE_MERGE_PATH, sheet_name=sheet)
        for sheet in pd.ExcelFile(EXCEL_PRE_MERGE_PATH).sheet_names
        if sheet != "Challenge"
    }

    with pd.ExcelWriter(EXCEL_MERGED_PATH) as writer:
        merged_df.to_excel(writer, sheet_name="Challenge", index=False)

        for sheet_name, df in other_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
