import random


def campi_vuoti(dati):
    for campo in dati.values():
        if campo == "":
            return True
    return False


def calcola_valore_rgb(squadra):
    somma_ascii = hash(squadra)
    r = somma_ascii % 209
    g = (somma_ascii // 2) % 209
    b = (somma_ascii // 3) % 209

    return r, g, b, 0.3
