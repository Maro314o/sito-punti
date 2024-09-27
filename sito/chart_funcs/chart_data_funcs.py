from sito.modelli import Cronologia


def elenco_punti_cumulativi(eventi: list[Cronologia], stagione: int) -> list[int]:
    return [evento.punti_cumulativi for evento in eventi if evento.stagione == stagione]


def elenco_date(eventi: list[Cronologia], stagione: int) -> list[str]:
    return [evento.data for evento in eventi if evento.stagione == stagione]
