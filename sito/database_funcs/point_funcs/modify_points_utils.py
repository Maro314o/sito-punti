from ..database_queries import cronologia_da_user
from ..list_database_elements import get_last_season
from ... import db
from ...modelli import Info


def aggiorna_punti_cumulativi(studente):
    punti_cumulativi = 0
    season = 1
    for evento in cronologia_da_user(studente):
        if season != evento.stagione:
            punti_cumulativi = 0
            season = evento.stagione
        punti_cumulativi += evento.modifica_punti
        evento.punti_cumulativi = punti_cumulativi
    db.session.commit()


def aggiorna_punti(utente):
    last_season_obj = Info.query.first()
    last_season = last_season_obj.last_season
    nuovi_punti = [0]

    for riga in cronologia_da_user(utente):
        if riga.stagione > last_season:
            last_season = riga.stagione
            last_season_obj.last_season = last_season
        while len(nuovi_punti) < riga.stagione:
            nuovi_punti.append(0)

        nuovi_punti[riga.stagione - 1] += riga.modifica_punti

    utente.punti = ",".join(map(str, nuovi_punti))
    utente.punti = utente.punti + ",0" * (last_season - len(utente.punti.split(",")))

    db.session.commit()
