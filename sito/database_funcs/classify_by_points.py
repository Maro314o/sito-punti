from sito.database_funcs.cronology_utils_funcs import ordina_cronologicamente
from sito.modelli.cronologia import Cronologia
from ..modelli import Utente, Classe
from itertools import accumulate


def classifica_user(stagione: int, utenti: list[Utente]) -> list[Utente]:
    """
    Ordina una lista di utenti in base ai punti ottenuti in una stagione.

    Args:
        stagione (int): Stagione di riferimento.
        utenti (list[Utente]): Lista di utenti da ordinare.

    Returns:
        list[Utente]: Lista di utenti ordinata dal punteggio più alto al più basso.
    """
    return sorted(
        utenti,
        key=lambda utente: utente.punti_stagione(stagione),
        reverse=True,
    )


def classifica_studenti_di_una_classe(stagione: int, classe: Classe) -> list[Utente]:
    """
    Ordina gli studenti di una classe in base ai punti della stagione.

    Args:
        stagione (int): Stagione di riferimento.
        classe (Classe): Istanza della classe.

    Returns:
        list[Utente]: Lista di studenti ordinata dal punteggio più alto al più basso.
    """
    studenti = classe.studenti.all()
    return classifica_user(stagione, studenti)


def classifica_studenti(stagione: int) -> list[Utente]:
    """
    Ordina tutti gli studenti in base ai punti della stagione.

    Args:
        stagione (int): Stagione di riferimento.

    Returns:
        list[Utente]: Lista di studenti ordinata dal punteggio più alto al più basso.
    """
    studenti = Utente.elenco_utenti()
    return classifica_user(stagione, studenti)


def classifica_squadre(classe: Classe, stagione: int) -> dict[str, float]:
    """
    Ordina le squadre di una classe in base ai punti della stagione.

    Args:
        classe (Classe): Istanza della classe.
        stagione (int): Stagione di riferimento.

    Returns:
        dict[str, float]: Dizionario con nome squadra come chiave e punteggio come valore,
                          ordinato dal punteggio più alto al più basso.
    """
    elenco_squadre = classe.squadre.all()
    punti_squadre = (
        (squadra.nome_squadra, squadra.punti_stagione(stagione)) for squadra in elenco_squadre
    )

    return dict(
        sorted(punti_squadre, key=lambda item: item[1], reverse=True)
    )


def ottieni_punti_parziali(eventi: list[Cronologia]) -> list[float]:
    """
    Calcola i punti parziali accumulati da una lista di eventi cronologici.

    Ordina gli eventi cronologicamente e restituisce una lista con i punteggi accumulati
    fino a ciascun evento.

    Args:
        eventi (list[Cronologia]): Lista di eventi Cronologia.

    Returns:
        list[float]: Lista dei punti accumulati.
    """
    eventi = ordina_cronologicamente(eventi)
    punti = [x.modifica_punti for x in eventi]
    return list(accumulate(punti))
