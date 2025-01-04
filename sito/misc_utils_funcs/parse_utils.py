import time
from datetime import datetime

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


def to_datetime_object(data: str) -> datetime:
    """
    converte una stringa che specifica la data con formato Y-m-d in un oggetto datetime
    """
    data = " ".join([data, "00:00:00"])
    return datetime.strptime(data, "%Y-%m-%d %H:%M:%S")


def get_season_points(points_str: str, season: int) -> float:
    """
    restituisce i punti di una persona in base alla stagione e stringa di punti
    """
    return float(points_str.split(",")[season - 1])


def set_season_points(points_str: str, season: int, points_to_set: float) -> str:
    """
    cambia i punti di una stagione in una stringa di punti
    """
    lista_punti = points_str.split(",")
    lista_punti[season - 1] = str(points_to_set)
    return ",".join(lista_punti)


def get_points_as_array(points_str: str) -> list[float]:
    return list(map(float, points_str.split(",")))


def convert_array_to_points_string(points_array: list[float]) -> str:
    return ",".join(list(map(str, points_array)))
