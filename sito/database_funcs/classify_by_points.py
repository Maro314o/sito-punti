from ..modelli import User, Classi
from .database_queries import studenti_da_classe
from .. import app

with app.app_context():
    from .list_database_elements import (
        elenco_studenti,
        elenco_squadre_da_classe,
        elenco_user_da_classe_id_e_nome_squadra,
    )

    def somma_punti_squadra(
        classe: Classi, nome_squadra: str, stagione_corrente: int
    ) -> float:
        """
        data una squadra si ottengono i punti totali di essa durante una stagione
        """
        studenti = elenco_user_da_classe_id_e_nome_squadra(classe.id, nome_squadra)
        punti_squadra = 0
        for studente in studenti:
            punti_squadra += float(studente.punti.split(",")[stagione_corrente - 1])
        return punti_squadra

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
        studenti = studenti_da_classe(classe)
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
        elenco_squadre = elenco_squadre_da_classe(classe)
        punti_squadre = {
            nome_squadra: somma_punti_squadra(classe, nome_squadra, stagione_corrente)
            for nome_squadra in elenco_squadre
        }

        return dict(
            sorted(punti_squadre.items(), key=lambda item: item[1], reverse=True)
        )
