import pandas as pd
from pathlib import Path
from os import path
import datetime

def refactor_file():
    from . import db

    from .modelli import User, Classi, Cronologia
    from .pagine_sito import classe_da_nome, user_da_email, elenco_admin, elenco_studenti, cronologia_da_user, user_da_nominativo



    db.session.query(Cronologia).delete()
    db.session.commit()
    error_file=path.join(Path.cwd(),'instance','errore.txt')
    log_file=path.join(Path.cwd(),'instance','log.txt')

    
    name_file=path.join(Path.cwd(),'instance','foglio.xlsx')
    file=pd.read_excel(name_file,sheet_name=None)
    dataset,*lista_fogli=file.keys()
    pd.to_datetime(file[dataset]['Data']) 
    error_file=path.join(Path.cwd(),'instance','errore.txt')
    with open(error_file,'w') as f:
        f.write('')

    for classe in lista_fogli:
        if not classe_da_nome(classe):
            nuova_classe=Classi(classe=classe)
            db.session.add(nuova_classe)
            db.session.commit()



        for riga in file[classe].values.tolist():
            
        
                nominativo=' '.join([x.strip().capitalize() for x in riga[0].strip().split()])
                print(nominativo)
                squadra=riga[1]
                if not user_da_nominativo(nominativo):
                    nuovo_utente = User(email=nominativo,nome='', cognome='',nominativo=nominativo,squadra=squadra,password='',punti='0',account_attivo=0,admin_user=0,classe_id=classe_da_nome(classe).id)
                    db.session.add(nuovo_utente)
                else:
                    user_da_nominativo(nominativo).squadra=squadra
                    user_da_nominativo(nominativo).classe=classe


    db.session.commit()

    for numero_riga,riga in enumerate(file[dataset].values.tolist()):
    #0 data
    #1 stagione
    #2 classe
    #3 alunno
    #4 attivita'
    #5 punti
        data=str(riga[0]).split()[0]
        stagione=riga[1]
        classe=riga[2]
        nominativo=' '.join([x.strip().capitalize() for x in riga[3].strip().split()])

        attivita=riga[4]
        punti=riga[5]
        print(nominativo)
        if not user_da_nominativo(nominativo):
            with open(error_file,'a') as f:
                f.write(f"{datetime.datetime.now()} | errore alla linea {numero_riga} del database : non è stato possibile modificare i punti dell\' utente {nominativo} della clase {classe}. Controlla se ci sono errori nella scrittura del suo nome o se non è stato aggiunto ad una classe nel corrispettivo foglio .xlsx\n")


            continue
        db.session.add(Cronologia(data=data,stagione=stagione,attivita=attivita,modifica_punti=punti,utente_id=user_da_nominativo(nominativo).id))
    db.session.commit()
    for utente in elenco_studenti():
        nuovi_punti=[0]


        for riga in cronologia_da_user(utente):
            
            while len(nuovi_punti)<riga.stagione:
                nuovi_punti.append(0)

            nuovi_punti[riga.stagione-1]+=riga.modifica_punti

        utente.punti=','.join(map(str,nuovi_punti))
    db.session.commit()

          
  
        
