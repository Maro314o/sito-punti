from sito.database_funcs import database_queries as db_queries, list_database_elements
from sito.misc_utils_funcs import parse_utils
from ..modelli import User, Classi

from .. import app

with app.app_context():
    from .list_database_elements import (
        elenco_studenti,
    )

    def classifica_user(stagione: int, users: list[User]) -> list[User]:
        """
        ordina una lista di utenti in base ai loro punti
        """
        return sorted(
            users,
            key=lambda user: float(user.punti.split(",")[stagione - 1]),
        )[::-1]

    def classifica_studenti_di_una_classe(stagione: int, classe: Classi) -> list[User]:
        """
        ordina una gli utenti di una classe in base ai loro punti
        """
        studenti = list_database_elements.elenco_studenti_da_classe(classe)
        return classifica_user(stagione, studenti)

    def classifica_studenti(stagione: int) -> list[User]:
        """
        ordina tutti gli studenti in base ai loro punti
        """
        studenti = elenco_studenti()
        return classifica_user(stagione, studenti)

    def classifica_squadre(
        classe: Classi, stagione_corrente: int
    ) -> dict[
        str, float
    ]:  # i dizionari mantengono l'ordine in cui la coppia chiave-valore e' stata aggiunta
        """
        ordina le squadre di una classe in base ai loro punti
        """
        elenco_squadre = list_database_elements.elenco_squadre_da_classe(classe)
        punti_squadre = {
            squadra.nome_squadra: parse_utils.get_season_points(
                squadra.punti_compensati, stagione_corrente
            )
            for squadra in elenco_squadre
        }

        return dict(
            sorted(punti_squadre.items(), key=lambda item: item[1], reverse=True)
        )
