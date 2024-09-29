ALLOWED_EXTENSIONS = set(["xlsx"])


def campi_vuoti(dati: dict[str, str]) -> bool:
    for campo in dati.values():
        if campo == "":
            return True
    return False


def allowed_files(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def calcola_valore_rgb(squadra: str) -> tuple[int, int, int, float]:
    somma_ascii = hash(squadra) * len(squadra)
    r = somma_ascii % 201
    g = (somma_ascii // 2) % 201
    b = (somma_ascii // 3) % 201

    return r, g, b, 0.3
