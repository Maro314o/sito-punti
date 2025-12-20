import json
import random
from sito.costanti import FRASI_PATH

ALLOWED_EXTENSIONS = {"xlsx"}


def allowed_files(filename: str) -> bool:
    """
    Verifica se il file ha un'estensione consentita.

    Args:
        filename (str): Nome del file da verificare.

    Returns:
        bool: True se il file ha un'estensione consentita, False altrimenti.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def calcola_valore_rgb(stringa: str) -> tuple[int, int, int, float]:
    """
    Genera un valore RGB dipendente dalla stringa.

    Args:
        stringa (str): Stringa da convertire in colore.

    Returns:
        tuple[int, int, int, float]: Tupla con valori RGB e alpha fisso a 0.3.
    """
    numero_hashato = hash(stringa) * len(stringa)
    r = numero_hashato % 201
    g = (numero_hashato // 2) % 201
    b = (numero_hashato // 3) % 201
    return r, g, b, 0.3


def is_empty(file_path: str) -> bool:
    """
    Verifica se un file di testo è vuoto.

    Args:
        file_path (str): Percorso del file.

    Returns:
        bool: True se il file è vuoto, False altrimenti.
    """
    with open(file_path, "r") as file:
        return file.read() == ""


def clear_file(file_path: str) -> None:
    """
    Elimina tutto il contenuto di un file di testo.

    Args:
        file_path (str): Percorso del file.
    """
    with open(file_path, "w") as file:
        file.write("")


def get_item_of_json(file_path: str, field: str) -> str | int:
    """
    Restituisce il valore di un campo da un file JSON.

    Args:
        file_path (str): Percorso del file JSON.
        field (str): Campo da leggere.

    Returns:
        str | int: Valore del campo specificato.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data[field]


def set_item_of_json(file_path: str, field: str, data: str) -> None:
    """
    Imposta un campo di un file JSON a un dato valore.

    Args:
        file_path (str): Percorso del file JSON.
        field (str): Campo da modificare.
        data (str): Nuovo valore del campo.
    """
    with open(file_path, "r") as file:
        json_data = json.load(file)
    json_data[field] = data
    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)


def query_json_by_nominativo_and_date(nominativo: str, data: str) -> str | None:
    """
    Cerca una frase in FRASI_PATH dato un nominativo e una data.

    Args:
        nominativo (str): Nome dell'autore della frase.
        data (str): Data della frase.

    Returns:
        str | None: Frase trovata, None se non presente.
    """
    with open(FRASI_PATH, "r") as file:
        json_data = json.load(file)
    for elemento in json_data:
        if elemento["autore"] == nominativo and elemento["data"] == data:
            return elemento["frase"]
    return None


def aggiungi_frase(autore: str, frase: str, data: str) -> None:
    """
    Aggiunge una nuova frase al file FRASI_PATH.

    Args:
        autore (str): Autore della frase.
        frase (str): Contenuto della frase.
        data (str): Data associata alla frase.
    """
    with open(FRASI_PATH, "r") as file:
        json_data = json.load(file)
    json_data.append({"autore": autore, "frase": frase, "data": data})
    with open(FRASI_PATH, "w") as file:
        json.dump(json_data, file, indent=4)


def rimuovi_frase(autore: str, data: str) -> bool:
    """
    Rimuove una frase dal file FRASI_PATH dato autore e data.

    Args:
        autore (str): Autore della frase.
        data (str): Data della frase.

    Returns:
        bool: True se è stata rimossa almeno una frase, False altrimenti.
    """
    with open(FRASI_PATH, "r") as file:
        json_data = json.load(file)
    lunghezza_iniziale = len(json_data)
    json_data = [x for x in json_data if x["autore"] != autore or x["data"] != data]
    with open(FRASI_PATH, "w") as file:
        json.dump(json_data, file, indent=4)
    return lunghezza_iniziale != len(json_data)


def get_random_json_item(file_path: str) -> str | int:
    """
    Restituisce un elemento casuale da un file JSON.

    Args:
        file_path (str): Percorso del file JSON.

    Returns:
        str | int: Elemento casuale del file.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return random.choice(data)


def append_to_file(file: str, contents: str) -> None:
    """
    Aggiunge una stringa alla fine di un file di testo.

    Args:
        file (str): Percorso del file.
        contents (str): Contenuto da aggiungere.
    """
    with open(file, "a") as f:
        f.write(contents)
