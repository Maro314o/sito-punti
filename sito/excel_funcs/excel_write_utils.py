import pandas as pd
from pathlib import Path
import openpyxl
import os
import sito.misc_utils_funcs as mc_utils

FILE_PATH = os.path.join(Path.cwd(), "data", "foglio.xlsx")


def aggiungi_riga_excel(
    data: str,
    stagione: int,
    classe: str,
    nominativo: str,
    attivita: str,
    punteggio: float,
) -> None:
    """
    aggiunge alla fine del file excel gia' salvato in memoria una riga con gli argomenti specificati
    """
    nuova_riga = [
        mc_utils.to_datetime_object(data),
        stagione,
        classe.upper(),
        nominativo.upper(),
        attivita,
        punteggio,
    ]
    wb = openpyxl.load_workbook(FILE_PATH)
    ws = wb.active
    ws.append(nuova_riga)
    wb.save(FILE_PATH)


def elimina_riga_excel(
    data: str,
    stagione: int,
    classe: str,
    nominativo: str,
    attivita: str,
    punteggio: float,
) -> None:
    """
    elimina la riga del file excel gia' salvato che corrisponde agli argomenti passati
    """
    valori_da_eliminare = [
        mc_utils.to_datetime_object(data),
        stagione,
        classe.upper(),
        nominativo.upper(),
        attivita,
        punteggio,
    ]

    dataframe = pd.read_excel(FILE_PATH, sheet_name=None)
    dataset, *_ = dataframe.keys()
    dataframe = dataframe[dataset]

    valore_riga_da_eliminare = dataframe.iloc[:, 0] == valori_da_eliminare[0]
    for index in range(1, len(valori_da_eliminare)):
        valore_riga_da_eliminare &= (
            dataframe.iloc[:, index] == valori_da_eliminare[index]
        )

    riga_da_eliminare = dataframe[valore_riga_da_eliminare].index
    dataframe = dataframe.drop(riga_da_eliminare[0])
    with pd.ExcelWriter(
        FILE_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        dataframe.to_excel(writer, sheet_name=dataset, index=False)
