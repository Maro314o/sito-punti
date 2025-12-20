import time
from datetime import datetime


def insert_underscore_name(stringa: str) -> str:
    """Sostituisce tutti gli spazi di una stringa con un underscore.

    Args:
        stringa (str): La stringa da trasformare.

    Returns:
        str: La stringa con gli spazi sostituiti da underscore.
    """
    return stringa.replace(" ", "_")


def remove_underscore_name(stringa: str) -> str:
    """Sostituisce tutti gli underscore di una stringa con uno spazio.

    Args:
        stringa (str): La stringa da trasformare.

    Returns:
        str: La stringa con gli underscore sostituiti da spazi.
    """
    return stringa.replace("_", " ")


def capitalize_all(stringa: str) -> str:
    """Rende maiuscola la prima lettera di ogni parola nella stringa.

    Args:
        stringa (str): La stringa da trasformare.

    Returns:
        str: La stringa con la prima lettera di ogni parola in maiuscolo.
    """
    stringa_list = stringa.split()
    stringa_list = [parola.capitalize() for parola in stringa_list]
    stringa = " ".join(stringa_list)
    return stringa


def converti_a_unix(data_str: str) -> int:
    """Converte una stringa di data in formato YYYY-MM-DD in Unix timestamp.

    Args:
        data_str (str): Data in formato 'YYYY-MM-DD'.

    Returns:
        int: Unix timestamp corrispondente alla mezzanotte della data.
    """
    data = datetime.strptime(data_str, "%Y-%m-%d")
    unix_timestamp = int(time.mktime(data.timetuple()))
    return unix_timestamp


def to_datetime_object(data: str) -> datetime:
    """Converte una stringa data in un oggetto datetime con ora impostata a mezzanotte.

    Args:
        data (str): Data in formato 'YYYY-MM-DD'.

    Returns:
        datetime: Oggetto datetime corrispondente alla data.
    """
    data = " ".join([data, "00:00:00"])
    return datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
