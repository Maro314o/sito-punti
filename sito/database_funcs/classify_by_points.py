from sito.database_funcs.cronology_utils_funcs import ordina_cronologicamente
from sito.modelli.cronologia import Cronologia
from ..modelli import Utente, Classe
from itertools import accumulate


def classifica_user(stagione: int, utenti: list[Utente]) -> list[Utente]:
    """
    ordina una lista di utenti in base ai loro punti
    """
    return sorted(
        utenti,
        key=lambda utente:utente.punti_stagione(stagione),
        reverse=True,
    )

def classifica_studenti_di_una_classe(stagione: int, classe: Classe) -> list[Utente]:
    """
    ordina una gli utenti di una classe in base ai loro punti
    """
    studenti = classe.studenti.all()
    return classifica_user(stagione, studenti)

def classifica_studenti(stagione: int) -> list[Utente]:
    """
    ordina tutti gli studenti in base ai loro punti
    """
    studenti = Utente.elenco_utenti()
    return classifica_user(stagione, studenti)

def classifica_squadre(
    classe: Classe, stagione: int
) -> dict[
    str, float
]:  # i dizionari mantengono l'ordine in cui la coppia chiave-valore e' stata aggiunta
    """
    ordina le squadre di una classe in base ai loro punti
    """
    elenco_squadre = classe.squadre.all()
    punti_squadre = (
        (squadra.nome_squadra, squadra.punti_stagione(stagione)) for squadra in elenco_squadre
    )

    return dict(
        sorted(punti_squadre, key=lambda item: item[1], reverse=True)
    )
def ottieni_punti_parziali(eventi : list[Cronologia]) -> list[float]:
    eventi=ordina_cronologicamente(eventi)
    punti = [x.modifica_punti for x in eventi]
    return     list(accumulate(punti))



