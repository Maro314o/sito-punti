import json
import random

from sito.costanti import FRASI_PATH

ALLOWED_EXTENSIONS = set(["xlsx"])


def allowed_files(filename: str) -> bool:
    """
    restituisce true se il file fa parte della lista delle estensioni supportate
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def calcola_valore_rgb(stringa: str) -> tuple[int, int, int, float]:
    """
    trasforma una stringa in un valore rgb dipendente da essa
    """
    numero_hashato = hash(stringa) * len(stringa)
    r = numero_hashato % 201
    g = (numero_hashato // 2) % 201
    b = (numero_hashato // 3) % 201

    return r, g, b, 0.3


def is_empty(file_path: str) -> bool:
    """
    se il file specificato e' vuoto ritorna True
    """
    with open(file_path, "r") as file:
        return file.read() == ""


def clear_file(file_path: str) -> None:
    """
    elimina tutti i contenuti di un file (di testo)
    """
    with open(file_path, "w") as file:
        file.write("")


def get_item_of_json(file_path: str, field: str) -> str | int:
    """
    ritorna un il valore di un campo di un file json
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data[field]

def query_json_by_nominativo_and_date(nominativo : str,data : str) -> str | None:
    """
    cerca una frase dal file delle frasi dato un nominativo e una data (in stringa)
    se non è presente ritorna None
    """
    with open(FRASI_PATH, "r") as file:
        json_data = json.load(file)
    frase = None
    for elemento in json_data:

        if elemento["autore"]==nominativo and elemento["data"]==data:
            frase = elemento["frase"] 
            break
    return frase
    

def set_item_of_json(file_path: str, field: str, data: str) -> None:
    """
    imposta il campo di un file json ad un certo dato
    """
    with open(file_path, "r") as file:
        json_data = json.load(file)
    json_data[field] = data
    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)


def get_random_json_item(file_path: str) -> str | int:
    """
    dato un file json restituisce un elemento a caso
    """

    with open(file_path, "r") as file:
        data = json.load(file)
    elemento_random = random.choice(data)
    return elemento_random


def append_to_file(file: str, contents: str) -> None:
    with open(file, "a") as f:
        f.write(contents)
