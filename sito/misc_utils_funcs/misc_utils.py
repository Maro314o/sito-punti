ALLOWED_EXTENSIONS = set(["xlsx"])


def campi_vuoti(dati: dict[str, str]) -> bool:
    """
    restituisce true se i campi di un form sono vuoti.
    """
    for campo in dati.values():
        if campo == "":
            return True
    return False


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
