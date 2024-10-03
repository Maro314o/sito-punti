import pandas as pd
from pathlib import Path
import os


def elimina_riga_excel(
    data: str,
    stagione: int,
    classe: str,
    nominativo: str,
    attivita: str,
    punteggio: float,
) -> None:
    valori_da_eliminare = [
        " ".join([data, "00:00:00"]),
        stagione,
        classe.upper(),
        nominativo.upper(),
        attivita,
        punteggio,
    ]

    FILE_PATH = os.path.join(Path.cwd(), "data", "foglio.xlsx")
    dataframe = pd.read_excel(FILE_PATH, sheet_name=None)
    dataset, *_ = dataframe.keys()
    dataframe = dataframe[dataset]

    valore_riga_da_eliminare = dataframe.iloc[:, 0] == valori_da_eliminare[0]
    for index in range(1, len(valori_da_eliminare)):
        valore_riga_da_eliminare &= (
            dataframe.iloc[:, index] == valori_da_eliminare[index]
        )

    riga_da_eliminare = dataframe[valore_riga_da_eliminare].index

    if riga_da_eliminare.empty:
        raise
    dataframe = dataframe.drop(riga_da_eliminare[0])
    with pd.ExcelWriter(
        FILE_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        # Salva il DataFrame modificato
        dataframe.to_excel(writer, sheet_name=dataset, index=False)
