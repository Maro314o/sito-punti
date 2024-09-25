def campi_vuoti(dati):
    for campo in dati.values():
        if campo == "":
            return True
    return False


def calcola_valore_rgb(squadra):
    somma_ascii = hash(squadra) * len(squadra)
    r = somma_ascii % 201
    g = (somma_ascii // 2) % 201
    b = (somma_ascii // 3) % 201

    return r, g, b, 0.3
