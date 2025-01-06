from sito.database_funcs import list_database_elements
import sito.database_funcs.database_queries as db_queries
from sito.misc_utils_funcs import parse_utils
from ..cronology_utils_funcs import cronologia_user
from ... import db
from ...modelli import Info, Squadra, User
import sito.database_funcs as db_funcs


def aggiorna_punti_cumulativi_eventi(studente: User) -> None:
    """
    per ogni evento di un utente assegna dei punti 'cumulativi'
    i puntunti cumulativi sono la somma dei punti di quell'evento e di tutti quelli precedenti cronologicamente
    """
    punti_cumulativi = 0.0
    season = 1
    for evento in cronologia_user(studente):
        if season != evento.stagione:
            punti_cumulativi = 0.0
            season = evento.stagione
        punti_cumulativi += evento.modifica_punti
        evento.punti_cumulativi = punti_cumulativi
    db.session.commit()


def aggiorna_punti_squadra(utente: User) -> None:
    """
    aggiunge i punti di un utente alla sua squadra
    """

    squadra = db_queries.squadra_da_id(utente.squadra_id)
    punti_utente = parse_utils.get_points_as_array(utente.punti)
    punti_squadra = parse_utils.get_points_as_array(squadra.punti_reali)
    punti_squadra.extend([0.0] * (len(punti_utente) - len(punti_squadra)))

    punti_squadra.extend([0.0] * (len(punti_utente) - len(punti_squadra)))
    for stagione, (punti_stagione_squadra, punti_stagione_utente) in enumerate(
        zip(punti_squadra, punti_utente)
    ):
        punti_squadra[stagione] = punti_stagione_squadra + punti_stagione_utente

    squadra.punti_reali = parse_utils.convert_array_to_points_string(punti_squadra)
    db.session.commit()


def compensa_punti_squadra(squadra: Squadra) -> None:
    """
    compensa il numero dei punti di una squadra
    """

    classe = db_queries.classe_da_id(squadra.classe_id)
    numero_membri_massimi = classe.massimo_studenti_squadra
    numero_membri_squadra = squadra.numero_componenti
    punti_squadra_reali = parse_utils.get_points_as_array(squadra.punti_reali)
    punti_squadra_compensati = parse_utils.get_points_as_array(squadra.punti_compensati)
    punti_squadra_compensati.extend(
        [0.0] * (len(punti_squadra_reali) - len(punti_squadra_compensati))
    )
    for stagione, punti_stagione_squadra in enumerate(punti_squadra_reali):
        punti_squadra_compensati[stagione] = (
            numero_membri_massimi * punti_stagione_squadra / numero_membri_squadra
        )
    squadra.punti_compensati = parse_utils.convert_array_to_points_string(
        punti_squadra_compensati
    )

    db.session.commit()


def aggiorna_punti(utente: User) -> None:
    """
    data un utente,si itera sulla sua cronolgia degli eventi e si sommano i punti di ogni evento
    per ottenere il totale dei punti di ogni stagione
    """
    last_season_obj = Info.query.first()
    last_season = last_season_obj.last_season
    nuovi_punti = [0]

    for riga in db_funcs.cronologia_user(utente):
        if riga.stagione > last_season:
            last_season = riga.stagione
            last_season_obj.last_season = last_season
        while len(nuovi_punti) < riga.stagione:
            nuovi_punti.append(0)

        nuovi_punti[riga.stagione - 1] += riga.modifica_punti

    utente.punti = ",".join(map(str, nuovi_punti))
    utente.punti = utente.punti + ",0.0" * (last_season - len(utente.punti.split(",")))

    db.session.commit()


def aggiorna_punti_composto(studente: User) -> None:
    """
    aggiorna tutti i punti dell'utente e della sua squadra
    """
    aggiorna_punti_cumulativi_eventi(studente)
    aggiorna_punti(studente)
    aggiorna_punti_squadra(studente)
    compensa_punti_squadra(db_queries.squadra_da_id(studente.squadra_id))
