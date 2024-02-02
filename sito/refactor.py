import pandas as pd
from pathlib import Path
from os import path
import datetime


def refactor_file():
    from . import db

    from .modelli import User, Classi, Cronologia, Info
    from .pagine_sito import (
        classe_da_nome,
        user_da_email,
        elenco_admin,
        elenco_studenti,
        cronologia_da_user,
        user_da_nominativo,
    )

    db.session.query(Cronologia).delete()
    db.session.commit()
    error_file = path.join(Path.cwd(), "instance", "errore.txt")
    log_file = path.join(Path.cwd(), "instance", "log.txt")
    name_file = path.join(Path.cwd(), "instance", "foglio.xlsx")
    file = pd.read_excel(name_file, sheet_name=None)
    dataset, *lista_fogli = file.keys()
    try:
        pd.to_datetime(file[dataset]["Data"])
    except:
        with open(error_file, "a") as f:
            f.write(
                f"{datetime.datetime.now()} | C'e' stato un errore nella conversione delle date\n"
            )

    error_file = path.join(Path.cwd(), "instance", "errore.txt")

    for classe in lista_fogli:
        if not classe_da_nome(classe):
            nuova_classe = Classi(classe=classe)
            db.session.add(nuova_classe)
            db.session.commit()

        for riga in file[classe].values.tolist():
            nominativo = " ".join(
                [x.strip().capitalize() for x in riga[0].strip().split()]
            )
            squadra = riga[1]
            if not user_da_nominativo(nominativo):
                nuovo_utente = User(
                    email=nominativo,
                    nome="",
                    cognome="",
                    nominativo=nominativo,
                    squadra=squadra,
                    password="",
                    punti="0",
                    account_attivo=0,
                    admin_user=0,
                    classe_id=classe_da_nome(classe).id,
                )
                db.session.add(nuovo_utente)
            else:
                user_da_nominativo(nominativo).squadra = squadra
                user_da_nominativo(nominativo).classe = classe

    db.session.commit()
    last_season = 0
    for numero_riga, riga in enumerate(file[dataset].values.tolist()):
        # 0 data
        # 1 stagione
        # 2 classe
        # 3 alunno
        # 4 attivita'
        # 5 punti
        data = str(riga[0]).split()[0]
        stagione = riga[1]
        classe = riga[2]
        nominativo = " ".join(
            [x.strip().capitalize() for x in str(riga[3]).strip().split()]
        )

        attivita = riga[4]
        punti = riga[5]
        if all(str(x).lower() == "nan" for x in riga):
            with open(error_file, "a") as f:
                f.write(
                    f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : La riga corrente e' vuota\n"
                )
            continue
        elif not user_da_nominativo(nominativo):
            with open(error_file, "a") as f:
                f.write(
                    f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : non è stato possibile modificare i punti dell' utente {nominativo} della classe {classe}. Controlla se ci sono errori nella scrittura del suo nome o se non è stato aggiunto ad una classe nel corrispettivo foglio .xlsx\n"
                )

            continue

        last_season = stagione if stagione > last_season else last_season

        db.session.add(
            Cronologia(
                data=data,
                stagione=stagione,
                attivita=attivita,
                modifica_punti=punti,
                punti_cumulativi=0,
                utente_id=user_da_nominativo(nominativo).id,
            )
        )
    db.session.query(Info).delete()
    db.session.commit()
    db.session.add(Info(last_season=last_season))
    db.session.commit()
    for utente in elenco_studenti():
        nuovi_punti = [0]

        for riga in cronologia_da_user(utente):
            while len(nuovi_punti) < riga.stagione:
                nuovi_punti.append(0)

            nuovi_punti[riga.stagione - 1] += riga.modifica_punti

        utente.punti = ",".join(map(str, nuovi_punti))
        utente.punti = utente.punti + ",0" * (
            last_season - len(utente.punti.split(","))
        )

    db.session.commit()
    studenti = elenco_studenti()
    for studente in studenti:
        punti_cumulativi = 0
        season = 1
        for evento in cronologia_da_user(studente):
            if season != evento.stagione:
                punti_cumulativi = 0
                season = evento.stagione
            punti_cumulativi += evento.modifica_punti
            evento.punti_cumulativi = punti_cumulativi
    db.session.commit()
