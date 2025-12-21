
from flask import (
    Blueprint,
    Response,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
)
from sito.costanti import ALLOWED_EXTENSIONS, COEFFICIENTI_ASSENZE, COEFFICIENTI_VOTI, CONFERMA_CAMBIAMENTI_DATABASE, DOWNLOAD_DIRECTORY_PATH, EXCEL_PRE_MERGE_PATH, FRASI_PATH, LEGGI,  NOMI_CHECKBOX, RETURN_VALUE, VERSION_PATH
from sito.errors_utils.errors_classes.data_error_classes import InvalidSeasonError
from sito.misc_utils_funcs.misc_utils import aggiungi_frase, query_json_by_nominativo_and_date, rimuovi_frase
from sito.modelli.classe import Classe
from sito.modelli.utente import Utente
from . import db, app

with app.app_context():
    import sito.database_funcs as db_funcs
import sito.misc_utils_funcs as mc_utils
import sito.excel_funcs as xlsx_funcs

from sito.errors_utils import admin_permission_required


from flask_login import login_required, current_user
from .modelli import Info, Cronologia
from .load_data import ERROR_FILE, GLOBAL_DATA, LOG_FILE, load_data, merge_excel

import datetime
import json

pagine_admin = Blueprint("pagine_admin", __name__)


@pagine_admin.route("/admin_dashboard")
@login_required
@admin_permission_required
def pagina_admin_dashboard() -> str:
    errori = not mc_utils.is_empty(ERROR_FILE)
    numero_degli_studenti = len(Utente.elenco_studenti())
    numero_delle_classi = len(Classe.elenco_classi_studenti())
    numero_degli_admin = len(Utente.elenco_admin())
    numero_studenti_registrati = len(Utente.elenco_studenti_registrati())
    numero_studenti_non_registrati = len(Utente.elenco_studenti_non_registrati())

    return render_template(
        "admin_dashboard.html",
        numero_studenti=numero_degli_studenti,
        Classe=Classe,
        numero_classi=numero_delle_classi,
        numero_admin=numero_degli_admin,
        numero_studenti_registrati=numero_studenti_registrati,
        numero_studenti_non_registrati=numero_studenti_non_registrati,
        novita=db_funcs.classifica_studenti(Info.ottieni_ultima_stagione())[0:8],
        errori=errori,
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
        last_season=Info.ottieni_ultima_stagione(),
    )


@pagine_admin.route("/classi", methods=["GET"])
@login_required
@admin_permission_required
def pagina_menu_classi() -> str:
    classi = Classe.elenco_classi_studenti()
    last_season = Info.ottieni_ultima_stagione()
    return render_template("menu_classi.html", classi=classi, last_season=last_season)


@pagine_admin.route("/db_errori")
@login_required
@admin_permission_required
def pagina_db_errori() -> str:
    with open(ERROR_FILE, LEGGI) as file_errore:
        content_error = file_errore.read().splitlines()
    return "<br><br>".join(content_error)


@pagine_admin.route("/versioni")
@login_required
@admin_permission_required
def pagina_versioni() -> str:
    return "<br>".join(reversed(open(VERSION_PATH, LEGGI).read().splitlines()))


@pagine_admin.route(
    "/classe/<classe_name>/<studente_id>/<int:stagione>/create_event", methods=["POST"]
)
@login_required
@admin_permission_required
def pagina_create_event(classe_name: str, studente_id: int, stagione: int) -> Response:
    data = request.form["data"]
    attivita = request.form["attivita"]
    modifica_punti = float(request.form["modifica_punti"])
    stagione = int(request.form["stagione"])

    if stagione > Info.ottieni_ultima_stagione():
        raise InvalidSeasonError("La season che hai inserito non esiste")
    xlsx_funcs.aggiungi_riga_excel(
        data,
        stagione,
        classe_name,
        Utente.da_id(studente_id).nominativo,
        attivita,
        modifica_punti,
    )
    nuovo_evento = Cronologia(
        utente_id=studente_id,
        stagione=stagione,
        data=data,
        attivita=attivita,
        modifica_punti=modifica_punti,
    )

    db.session.add(nuovo_evento)
    db.session.commit()


    mc_utils.set_item_of_json(
        GLOBAL_DATA, "ultima_modifica", str(datetime.datetime.now().date())
    )
    return redirect(
        url_for(
            "pagine_admin.pagina_info_studente",
            classe_name=classe_name,
            nominativo_con_underscore="_".join(
                Utente.da_id(studente_id).nominativo.split()
            ),
            stagione=stagione,
        )
    )


@pagine_admin.route(
    "/classe/<classe_name>/<studente_id>/<stagione>/delete_event/<int:event_id>",
    methods=["POST"],
)
@login_required
@admin_permission_required
def pagina_delete_event(
    classe_name: str, studente_id: int, stagione: int, event_id: int
) -> Response:
    evento = Cronologia.da_id(event_id)
    xlsx_funcs.elimina_riga_excel(
        evento.data,
        evento.stagione,
        classe_name,
        Utente.da_id(studente_id).nominativo,
        evento.attivita,
        evento.modifica_punti,
    )
    if evento:
        db.session.delete(evento)


        mc_utils.set_item_of_json(
            GLOBAL_DATA, "ultima_modifica", str(datetime.datetime.now().date())
        )
        flash("Evento eliminato con successo", "success")
    else:
        flash("Evento non trovato", "error")

    return redirect(
        url_for(
            "pagine_admin.pagina_info_studente",
            classe_name=classe_name,
            nominativo_con_underscore=mc_utils.insert_underscore_name(
                Utente.da_id(studente_id).nominativo
            ),
            stagione=stagione,
        )
    )


@pagine_admin.route("/elenco_user/<elenco_type>", methods=["GET"])
@login_required
@admin_permission_required
def pagina_elenco_user_display(elenco_type: str) -> str:
    if elenco_type == "tutti_gli_studenti_registrati":
        utenti = Utente.elenco_studenti_registrati()

    elif elenco_type == "studenti_non_registrati":
        utenti = Utente.elenco_studenti_non_registrati()

    elif elenco_type == "tutti_gli_admin":
        utenti = Utente.elenco_admin()
    else:
        utenti = Utente.elenco_studenti()
    return render_template(
        "elenco_user.html", utenti=utenti,Classe=Classe
    )


@pagine_admin.route("/gestione_dati/<classe_name>/", 
    methods=["GET", "POST"]
)
@login_required
@admin_permission_required
def pagina_gestione_dati_r(classe_name:str) -> str:
    return redirect(url_for("pagine_admin.pagina_gestione_dati",classe_name=classe_name,data_str='none'))

@pagine_admin.route("/gestione_dati/<classe_name>/<data_str>", 
    methods=["GET", "POST"]
)
@login_required
@admin_permission_required
def pagina_gestione_dati(classe_name:str,data_str:str) -> Response | str:
    data_str = datetime.datetime.today().strftime('%Y-%m-%d') if data_str=="none" else data_str
    elenco_classi =[x.nome_classe for x in Classe.elenco_classi_studenti()]
    if request.method == "POST":
        returned_form = request.form
        form_id = returned_form.get("form_id")
        if form_id == "classSelector":
            classe_name = returned_form["classSelector"]
            return redirect(url_for("pagine_admin.pagina_gestione_dati",classe_name=classe_name,data_str=data_str))
        elif form_id == "dateSelector":
            data_str = returned_form["dateSelector"]

            return redirect(url_for("pagine_admin.pagina_gestione_dati",classe_name=classe_name,data_str=data_str))

        elif form_id == "students_data":
            valori_ritornati={str(x.id):{"USER":x} for x in Classe.da_nome(classe_name).studenti.all()}

            for identificativo,valore in returned_form.items():
                if identificativo == "form_id": continue
                Uid,tipo,*numero_identificativo=identificativo.split('_')
                if tipo == "Voto" or tipo == "tipo-Voto":
                    numero_identificativo = numero_identificativo[0]
                    if "Voto" not in valori_ritornati[Uid]:
                        valori_ritornati[Uid]["Voto"]={}
                    if  numero_identificativo not in valori_ritornati[Uid]["Voto"]:
                        valori_ritornati[Uid]["Voto"][numero_identificativo]={}
                    valori_ritornati[Uid]["Voto"][numero_identificativo][tipo]=valore
                    continue


                valori_ritornati[Uid][tipo] = valore
            stagione = Info.ottieni_ultima_stagione()

            for Uid,value_dict in valori_ritornati.items():
                user = value_dict["USER"]
                eventi_da_eliminare = user.cronologia_studente.filter_by(data=data_str).all()
                rimuovi_frase(user.nominativo,data_str)
                for evento in eventi_da_eliminare:
                    db.session.delete(evento)
                for tipo,valore in value_dict.items():
                    attivita = None
                    punti = None
                    if tipo in NOMI_CHECKBOX:
                        attivita=tipo
                        punti = float(NOMI_CHECKBOX[tipo])
                    elif tipo == "Stato" and valore != "Presente":
                            attivita=valore
                            punti=float(COEFFICIENTI_ASSENZE[valore])
                    elif tipo=="Voto" :
                        for _,valutazione in valore.items(): 
                            if valutazione["Voto"]== "": continue
                            db.session.add(
                                    Cronologia(
                                        data= data_str,
                                        stagione = stagione,
                                        attivita=valutazione["tipo-Voto"],
                                        modifica_punti=COEFFICIENTI_VOTI[valutazione["tipo-Voto"]]*float(valutazione["Voto"]),
                                        utente_id=user.id
                                        ))
                        continue
                    elif tipo == "frase-del-giorno" and valore !="":
                        aggiungi_frase(user.nominativo,valore,data_str)
                        attivita="Frase"
                        punti=1.0
                    if attivita and punti:
                        db.session.add(
                                    Cronologia(
                                        data= data_str,
                                        stagione = stagione,
                                        attivita=attivita,
                                        modifica_punti=punti,
                                        utente_id=user.id
                                        ))
                db.session.commit()                 
        else:
            print("you alone in this one lil blud")
    if classe_name=="admin":
        classe_name="none"
    if classe_name != "none":
        lista_studenti_v=[[x,dict()] for x in Classe.da_nome(classe_name).studenti.all()]
        lista_studenti_v.sort(key=lambda x: x[0].nominativo)

        if Cronologia.query.filter_by(data=data_str).first() is not None:
            for ind,(studente,_) in enumerate(lista_studenti_v):
                frase = query_json_by_nominativo_and_date(studente.nominativo,data_str)
                if frase is not None:
                    lista_studenti_v[ind][1]["frase"]=frase
                cron = studente.cronologia_studente.filter_by(data=data_str).all()
                for evento in cron:
                    v = 1
                    if evento.attivita in COEFFICIENTI_VOTI:
                        v = evento.modifica_punti/COEFFICIENTI_VOTI[evento.attivita]
                        if 'Voto' in lista_studenti_v[ind][1]:
                            lista_studenti_v[ind][1]['Voto'].append((evento.attivita,v))
                        else:
                            lista_studenti_v[ind][1]['Voto']=[(evento.attivita,v)]
                        continue
                    lista_studenti_v[ind][1][evento.attivita]=v
                
    else:
        lista_studenti_v=None

    return render_template(
    "manage_data.html",classe_name=classe_name,elenco_classi=elenco_classi,data=data_str,lista_studenti_v=lista_studenti_v
     )





@pagine_admin.route("/load_db", methods=["POST"])
@login_required
@admin_permission_required
def pagina_load_db() -> Response:
    if request.method == "POST":
        dati = request.form
        if dati[RETURN_VALUE] == CONFERMA_CAMBIAMENTI_DATABASE:
            file = request.files["file_db"]
            if not mc_utils.allowed_files(file.filename):
                with open(ERROR_FILE, "w") as f:
                    f.write(
                        f"Impossibile aprire questa estensione dei file, per adesso puoi caricare il database sono in questo/i formato/i : {ALLOWED_EXTENSIONS}"
                    )

                return redirect(url_for("pagine_admin.pagina_gestione_dati"))
            file.save(EXCEL_PRE_MERGE_PATH)
            merge_excel()
            load_data(current_user)

    return redirect(url_for("pagine_admin.pagina_gestione_dati"))


@app.route("/download/<filename>")
@login_required
@admin_permission_required
def download_file(filename):
    return send_from_directory(DOWNLOAD_DIRECTORY_PATH, filename, as_attachment=True)


@app.route("/log_excel")
@login_required
@admin_permission_required
def pagina_log_excel():
    return "<br>".join(reversed(open(LOG_FILE, LEGGI).read().splitlines()))


@pagine_admin.route("/aggiunta_frase", methods=["POST"])
@login_required
@admin_permission_required
def pagina_aggiungi_frase() -> Response:
    frase = request.form["frase"]
    autore = request.form["autore"]
    with open(FRASI_PATH, "r") as file:
        json_data = json.load(file)
    json_data.append(
        {
            "autore": str(autore),
            "frase": str(frase),
            "data": str(datetime.datetime.now().date()),
        }
    )
    with open(FRASI_PATH, "w") as file:
        json.dump(json_data, file, indent=4)
    return redirect(url_for("pagine_admin.pagina_gestione_dati"))
