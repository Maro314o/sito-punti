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
    stringa_list = stringa.split()
    stringa_list = [parola.capitalize() for parola in stringa_list]
    stringa = " ".join(stringa_list)
    return stringa


def converti_a_unix(data_str: str) -> int:
    """
    converte una stringa data in formato y-m-d nella corrispondente unix timestamp
    """
    data = datetime.strptime(data_str, "%Y-%m-%d")

    unix_timestamp = int(time.mktime(data.timetuple()))

    return unix_timestamp


def to_datetime_object(data: str) -> datetime:
    """
    converte una stringa che specifica la data con formato Y-m-d in un oggetto datetime
    """
    data = " ".join([data, "00:00:00"])
    return datetime.strptime(data, "%Y-%m-%d %H:%M:%S")




