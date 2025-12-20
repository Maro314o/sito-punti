from sito.modelli import Cronologia
from ..misc_utils_funcs import converti_a_unix


def ordina_cronologicamente(lista_cronologia: list[Cronologia]) -> list[Cronologia]:
    """
    Ordina una lista di eventi Cronologia in ordine cronologico.

    Args:
        lista_cronologia (list[Cronologia]): Lista di oggetti Cronologia da ordinare.

    Returns:
        list[Cronologia]: Lista ordinata cronologicamente in base alla data.
    """
    return sorted(lista_cronologia, key=lambda evento: converti_a_unix(evento.data))
