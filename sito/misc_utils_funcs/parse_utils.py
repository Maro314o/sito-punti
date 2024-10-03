import time
from datetime import datetime


def insert_underscore_name(stringa: str) -> str:
    """
    sostituisce tutti gli spazi di una stringa con un underscore
    """
    return stringa.replace(" ", "_")


def remove_underscore_name(stringa: str) -> str:
    """
    sostituisce tutti gli underscore di una stringa con uno spazio
    """
    return stringa.replace("_", " ")


def capitalize_all(stringa: str) -> str:
    """
    data una stringa la restituisce facendo diventare maiuscole la prima lettera di ogni parola separata da uno spazio
    """
    stringa = stringa.split()
    stringa = [parola.capitalize() for parola in stringa]
    stringa = " ".join(stringa)
    return stringa


def converti_a_unix(data_str: str) -> int:
    """
    converte una stringa data in formato y-m-d nella corrispondente unix timestamp
    """
    data = datetime.strptime(data_str, "%Y-%m-%d")

    unix_timestamp = int(time.mktime(data.timetuple()))

    return unix_timestamp
