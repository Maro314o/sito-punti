from pathlib import Path
import json

# === DIRECTORY PATHS ===
CURRENT_WORKING_DIRECTORY_PATH: str = str(Path.cwd())
DATA_DIRECTORY_PATH: str = str(Path(CURRENT_WORKING_DIRECTORY_PATH) / "data")
SECRETS_DIRECTORY_PATH: str = str(Path(CURRENT_WORKING_DIRECTORY_PATH) / "secrets")
DOWNLOAD_DIRECTORY_PATH: str = DATA_DIRECTORY_PATH
STATIC_DIRECTORY_PATH: str = str(Path(CURRENT_WORKING_DIRECTORY_PATH) / "sito" / "static")
TEMPLATE_DIRECTORY_PATH: str = str(Path(STATIC_DIRECTORY_PATH) / "html")
LOGHI_DIRECTORY_PATH: str = str(Path(STATIC_DIRECTORY_PATH) / "images" / "loghi")

# === FILE PATHS ===
ERROR_PATH: str = str(Path(DATA_DIRECTORY_PATH) / "errore.txt")
LOG_PATH: str = str(Path(DATA_DIRECTORY_PATH) / "log.txt")
EXCEL_PRE_MERGE_PATH: str = str(Path(DATA_DIRECTORY_PATH) / "foglio_pre-merge.xlsx")
EXCEL_MERGED_PATH: str = str(Path(DATA_DIRECTORY_PATH) / "foglio.xlsx")
GLOBAL_DATA_PATH: str = str(Path(DATA_DIRECTORY_PATH) / "global_data.json")
VERSION_PATH: str = str(Path(DATA_DIRECTORY_PATH) / "versioni.txt")
FRASI_PATH: str = str(Path(DATA_DIRECTORY_PATH) / "frasi.json")
SECRET_KEY_PATH: str = str(Path(SECRETS_DIRECTORY_PATH) / "secret_token.txt")
SECRET_PASSWORD_PATH: str = str(Path(SECRETS_DIRECTORY_PATH) / "secret_starter_admin_password.txt")

# === INIT VALUES ===
INIT_BASE_KEY: str = "standardbasekey"
INIT_GLOBAL_DATA: str = json.dumps({"stagione": 0, "ultimo_upload": 0, "ultima_modifica": 0})
INIT_FRASE: str = json.dumps([
    {
        "autore": "anonimo",
        "frase": "Ci sono 10 tipi di persone al mondo: quelle che capiscono il codice binario e quelle che non lo capiscono.",
        "data": "1970-01-01"
    }
])

# === DATABASE ===
DB_NAME: str = "database.db"
DATABASE_LOCATION_URL: str = f"sqlite:///{Path(DATA_DIRECTORY_PATH) / DB_NAME}"

# === MISC ===
MESI: dict[str, int] = {
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

COEFFICIENTI_VOTI: dict[str, int] = {
    "Verifica": 3,
    "Interrogazione": 2,
    "Progetto": 2
}

SELECTORS ={
"Presenza" : {
    "Presente":0,
    "Assenza": -1,
    "Assenza+": -3
}
}
COEFFICIENTI_ASSENZE = SELECTORS["Presenza"]

NOMI_CHECKBOX: dict[str, int] = {
    "Bug": 1,
    "Cellulare": 1,
    "Beccato Cellulare": -1,
    "Multiverso": 3,
    "Ansia": -3,
    "Memoria": 2,
    "Lessico": 1,
    "Nota": 1
}

# === STRINGHE UTILI ===
VUOTO: str = ""
LEGGI: str = "r"
RETURN_VALUE: str = "bottone"
ELIMINA_UTENTE: str = "elimina"
AGGIUNGI_CLASSE: str = "nuova"
ENTRA_NELLA_CLASSE: str = "raggiunti"
CONFERMA_CAMBIAMENTI_DATABASE: str = "load_database"

# === ALTRI SET ===
ALLOWED_EXTENSIONS = frozenset(["xlsx"])
NOT_AVALIDABLE = frozenset(["admin", "Nessuna_squadra"])
