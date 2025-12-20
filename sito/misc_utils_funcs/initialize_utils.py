import os


def init_directory(directory_path: str) -> None:
    """
    Crea una directory se non esiste già.

    Args:
        directory_path (str): Percorso della directory da creare.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def init_file(file_path: str, message: str = "") -> None:
    """
    Crea un file se non esiste già e opzionalmente vi scrive un messaggio iniziale.

    Args:
        file_path (str): Percorso del file da creare.
        message (str, optional): Contenuto iniziale da scrivere nel file. Defaults to "".
    """
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write(message)
