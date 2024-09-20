import pandas as pd
from pathlib import Path
from os import path
import datetime

from sito.database_funcs.database_queries import user_da_nominativo
from sito.database_funcs.list_database_elements import elenco_classi_studenti

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


def refactor_file(current_user):
    from . import db

    from .modelli import User, Classi, Cronologia, Info
    import sito.database_funcs as db_funcs

    db.session.query(Cronologia).delete()

    db.session.query(Info).delete()

    User.query.filter_by(account_attivo=0).delete()
    db.session.query(Classi).delete()
    db.session.add(Classi(classe="admin"))
    db.session.commit()
    error_file = path.join(Path.cwd(), "data", "errore.txt")
    log_file = path.join(Path.cwd(), "data", "log.txt")
    name_file = path.join(Path.cwd(), "data", "foglio.xlsx")
    file = pd.read_excel(name_file, sheet_name=None)
    dataset, *lista_fogli = file.keys()

    errori = 0
    for classe in lista_fogli:
        nuova_classe = Classi(classe=classe)
        db.session.add(nuova_classe)
        db.session.commit()

        for numero_riga, riga in enumerate(file[classe].values.tolist()):
            nominativo = " ".join(
                [x.strip().capitalize() for x in riga[0].strip().split()][0:2]
            )
            if len(riga) == 1:
                with open(error_file, "a") as f:
                    f.write(
                        f"{datetime.datetime.now()} | errore alla linea {numero_riga} del foglio {classe} del edatabase : La cella della squadra per questo utente e' vuota.Gli verra' assegnata una squadra provvisoria chiamata \"Nessuna_squadra\"\n"
                    )
                squadra = "Nessuna_squadra"
            else:
                squadra = riga[1]
            utente = user_da_nominativo(nominativo)
            if not utente:
                utente = User(
                    email=f"email_non_registrata_per_{'_'.join(nominativo.split())}",
                    nome=nominativo.split()[1],
                    cognome=nominativo.split()[0],
                    nominativo=nominativo,
                    squadra=squadra,
                    password="",
                    punti="0",
                    account_attivo=0,
                    admin_user=0,
                    classe_id=db_funcs.classe_da_nome(classe).id,
                )
                db.session.add(utente)
            else:
                utente.squadra = squadra
                utente.punti = "0"
                utente.classe_id = db_funcs.classe_da_nome(classe).id

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
        classe = riga[2]
        nominativo = " ".join(
            [x.strip().capitalize() for x in str(riga[3]).strip().split()][0:2]
        )

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
                    f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : non è stato possibile modificare i punti dell' utente {nominativo} della classe {classe}. Controlla se ci sono errori nella scrittura del suo nome o se non è stato aggiunto ad una classe nel corrispettivo foglio .xlsx\n"
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
        if not (db_funcs.classe_da_id(utente.classe_id) in elenco_classi_studenti()):
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
