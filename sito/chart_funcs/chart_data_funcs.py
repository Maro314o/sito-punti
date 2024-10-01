from sito.modelli import Cronologia


def elenco_punti_cumulativi(eventi: list[Cronologia], stagione: int) -> list[int]:
    """
    data la cronologia degli eventi di uno studente
    restituisce i punti cumulativi degli eventi di una stagione
    """
    return [evento.punti_cumulativi for evento in eventi if evento.stagione == stagione]


def elenco_date(eventi: list[Cronologia], stagione: int) -> list[str]:
    """
    data la cronologia degli eventi di uno studente
    restituisce le date degli eventi di una stagione
    """
    return [evento.data for evento in eventi if evento.stagione == stagione]


def elenco_attivita(eventi: list[Cronologia], stagione: int) -> list[str]:
    """
    data la cronologia degli eventi di uno studente
    restituisce le attività degli eventi di una stagione
    """
    return [evento.attivita for evento in eventi if evento.stagione == stagione]
