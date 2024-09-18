def campi_vuoti(dati):
    for campo in dati.values():
        if campo == "":
            return True
    return False


def calcola_valore_rgb(squadra):
    somma_ascii = sum(ord(char) ** len(squadra) for char in squadra) + 70
    r = somma_ascii % 256
    g = (somma_ascii // 2) % 256
    b = (somma_ascii // 3) % 256

    return r, g, b, 0.3
