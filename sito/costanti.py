from os import path
from pathlib import Path

# DIRECTORY PATH
CURRENT_WORKING_DIRECTORY_PATH = Path.cwd()
DATA_DIRECTORY_PATH = path.join(CURRENT_WORKING_DIRECTORY_PATH, "data")
SECRETS_DIRECTORY_PATH = path.join(CURRENT_WORKING_DIRECTORY_PATH, "secrets")
DOWNLOAD_DIRECTORY_PATH = DATA_DIRECTORY_PATH
STATIC_DIRECTORY_PATH = path.join(CURRENT_WORKING_DIRECTORY_PATH, "sito", "static")
TEMPLATE_DIRECTORY_PATH = path.join(STATIC_DIRECTORY_PATH, "html")
LOGHI_DIRECTORY_PATH = path.join(STATIC_DIRECTORY_PATH, "images", "loghi")
# FILE PATH
ERROR_PATH = path.join(DATA_DIRECTORY_PATH, "errore.txt")
LOG_PATH = path.join(DATA_DIRECTORY_PATH, "log.txt")
EXCEL_PRE_MERGE_PATH = path.join(DATA_DIRECTORY_PATH, "foglio_pre-merge.xlsx")
GLOBAL_DATA_PATH = path.join(DATA_DIRECTORY_PATH, "global_data.json")
VERSION_PATH = path.join(DATA_DIRECTORY_PATH, "versioni.txt")
FRASI_PATH = path.join(DATA_DIRECTORY_PATH, "frasi.json")
EXCEL_MERGED_PATH = path.join(DATA_DIRECTORY_PATH, "foglio.xlsx")
SECRET_KEY_PATH = path.join(SECRETS_DIRECTORY_PATH, "secret_token.txt")
SECRET_PASSWORD_PATH = path.join(
    SECRETS_DIRECTORY_PATH, "secret_starter_admin_password.txt"
)

# INIT VALUES COSTANTS

INIT_BASE_KEY = "standardbasekey"
INIT_GLOBAL_DATA = '{"stagione":0,"ultimo_upload":0,"ultima_modifica":0}'
INIT_FRASE = '[{"autore":"anonimo","frase":"Ci sono 10 tipi di persone al mondo: quelle che capiscono il codice binario e quelle che non lo capiscono.","data":"1970-1-1"}]'

# DATABASE THINGS

DB_NAME = "database.db"
DATABASE_LOCATION_URL = f"sqlite:///{path.join(DATA_DIRECTORY_PATH, DB_NAME)}"


# MISC COSTANTS
MESI = {
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
COEFFICIENTI_VOTI ={"Verifica" : 3,"Interrogazione":2,"Progetto":2}
NOMI_CHECKBOX= {"Bug":1, "Cellulare":1, "Cellulare_minus":-1, "Multiverso":3, "Ansia":-3, "Memoria":2, "Lessico":1, "Nota":1}
VUOTO = ""
ERROR = True
NO_ERROR = False

ALLOWED_EXTENSIONS = set(["xlsx"])
NOT_AVALIDABLE = ["admin", "Nessuna_squadra"]

LEGGI = "r"
RETURN_VALUE = "bottone"
ELIMINA_UTENTE = "elimina"
AGGIUNGI_CLASSE = "nuova"
ENTRA_NELLA_CLASSE = "raggiunti"
CONFERMA_CAMBIAMENTI_DATABASE = "load_database"
