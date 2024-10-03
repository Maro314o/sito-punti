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
