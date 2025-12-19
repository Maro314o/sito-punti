from sito.modelli import Cronologia
from ..misc_utils_funcs import converti_a_unix


def ordina_cronologicamente(lista_cronologia: list[Cronologia]) -> list[Cronologia]:
    """
    ordina gli eventi di una cronologia in ordine cronologico
    """
    return sorted(lista_cronologia, key=lambda evento: converti_a_unix(evento.data))


