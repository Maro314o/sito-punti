from ..modelli import User, Classe
from .database_queries import studenti_da_classe
from .. import app

with app.app_context():
    from .list_database_elements import elenco_studenti

    def classifica_user(stagione: int, users: list[User]) -> list[User]:
        return sorted(
            users,
            key=lambda user: float(user.punti.split(",")[stagione - 1]),
        )[::-1]

    def classifica_studenti_di_una_classe(stagione: int, classe: Classe) -> list[User]:
        studenti = studenti_da_classe(classe)
        return classifica_user(stagione, studenti)

    def classifica_studenti(stagione: int) -> list[User]:
        studenti = elenco_studenti()
        return classifica_user(stagione, studenti)
