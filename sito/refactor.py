import pandas as pd
from pathlib import Path
from os import path
import datetime

from .modelli import User
from sito.database_funcs.database_queries import user_da_nominativo
import sito.misc_utils_funcs as mc_utils

mesi = {
    "gennaio": 1,
    "febbraio": 2,
    "marzo": 3,
    "aprile": 4,
    "maggio": 5,
    "giugno": 6,
    "luglio": 7,
    "agosto": 8,
    "settembre": 9,
    "ottobre": 10,
    "novembre": 11,
    "dicembre": 12,
}


def refactor_file(current_user: User) -> None:
    from . import db

    from .modelli import User, Classi, Cronologia, Info
    import sito.database_funcs as db_funcs

    db.session.query(Cronologia).delete()

    db.session.query(Info).delete()

    User.query.filter_by(account_attivo=0).delete()
    db.session.query(Classi).delete()
    db_funcs.crea_classe("admin")
    db.session.commit()
    error_file = path.join(Path.cwd(), "data", "errore.txt")
    log_file = path.join(Path.cwd(), "data", "log.txt")
    name_file = path.join(Path.cwd(), "data", "foglio.xlsx")
    file = pd.read_excel(name_file, sheet_name=None)
    dataset, *lista_fogli = file.keys()
    nominativi_trovati = set()
    errori = 0
    for classe_name in lista_fogli:
        db_funcs.crea_classe(classe_name)
        for numero_riga, riga in enumerate(file[classe_name].values.tolist()):
            nominativo = riga[0]
            nominativo = mc_utils.capitalize_all(nominativo)
            if len(riga) == 1:

                with open(error_file, "a") as f:
                    f.write(
                        f"{datetime.datetime.now()} | errore alla linea {numero_riga} del foglio {classe_name} del edatabase : La cella della squadra per questo utente e' vuota.Gli verra' assegnata una squadra provvisoria chiamata \"Nessuna_squadra\"\n"
                    )
                squadra = "Nessuna_squadra"
            else:
                squadra = riga[1]
            utente = user_da_nominativo(nominativo)
            nominativi_trovati.add(nominativo)
            if not utente:
                db_funcs.crea_user(
                    email=f"email_non_registrata_per_{'_'.join(nominativo.split())}",
                    nominativo=nominativo,
                    squadra=squadra,
                    password="",
                    account_attivo=0,
                    classe_name=classe_name,
                )
            else:
                utente.nominativo = nominativo
                utente.squadra = squadra
                utente.punti = "0"
                utente.classe_id = db_funcs.classe_da_nome(classe_name).id

    db.session.commit()
    last_season = 0
    for numero_riga, riga in enumerate(file[dataset].values.tolist()):
        # 0 data
        # 1 stagione
        # 2 classe
        # 3 alunno
        # 4 attivita'
        # 5 punti
        data = str(riga[0]).split()

        try:
            data = f"{data[1]}/{mesi[data[2]]}/{data[3]}"
        except:
            data = data[0]
        stagione = riga[1]
        classe_name = riga[2]
        nominativo = mc_utils.capitalize_all(riga[3])

        attivita = riga[4]
        punti = riga[5]
        if all(str(x).lower() == "nan" for x in riga):
            with open(error_file, "a") as f:
                f.write(
                    f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : La riga corrente e' vuota\n"
                )
            errori += 1
            continue
        elif not db_funcs.user_da_nominativo(nominativo):
            with open(error_file, "a") as f:
                f.write(
                    f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : non è stato possibile modificare i punti dell' utente {nominativo} della classe {classe_name}. Controlla se ci sono errori nella scrittura del suo nome o se non è stato aggiunto ad una classe nel corrispettivo foglio .xlsx\n"
                )
            errori += 1

            continue

        last_season = stagione if stagione > last_season else last_season
        db.session.add(
            Cronologia(
                data=data,
                stagione=stagione,
                attivita=attivita,
                modifica_punti=punti,
                punti_cumulativi=0,
                utente_id=db_funcs.user_da_nominativo(nominativo).id,
            )
        )
    db.session.query(Info).delete()
    db.session.add(Info(last_season=last_season))
    db.session.commit()
    for utente in db_funcs.elenco_studenti():
        if utente.nominativo not in nominativi_trovati:
            db.session.delete(utente)
    db.session.commit()
    for utente in db_funcs.elenco_studenti():
        db_funcs.aggiorna_punti(utente)

    studenti = db_funcs.elenco_studenti()
    for studente in studenti:
        db_funcs.aggiorna_punti_cumulativi(studente)
    with open(log_file, "a") as f:
        f.write(
            f"{datetime.datetime.now()} | {current_user.nominativo} ha appena caricato un file excel con {errori} errori\n"
        )
