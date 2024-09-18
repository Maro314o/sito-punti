from .database_queries import studenti_da_classe

from .. import app

with app.app_context():
    from .list_database_elements import elenco_studenti

    def classifica_user(stagione, studenti):
        return sorted(
            studenti,
            key=lambda studente: float(studente.punti.split(",")[stagione - 1]),
        )[::-1]

    def classifica_studenti_di_una_classe(stagione, classe):
        studenti = studenti_da_classe(classe)
        return classifica_user(stagione, studenti)

    def classifica_studenti(stagione):
        studenti = elenco_studenti()
        return classifica_user(stagione, studenti)
