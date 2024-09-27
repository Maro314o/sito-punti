from sito.modelli import Cronologia


def list_data(eventi: list[Cronologia], stagione: int) -> list[int]:
    return [evento.punti_cumulativi for evento in eventi if evento.stagione == stagione]


def list_label(eventi: list[Cronologia], stagione: int) -> list[str]:
    return [evento.data for evento in eventi if evento.stagione == stagione]
