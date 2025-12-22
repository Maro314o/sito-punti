
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
from sito.costanti import ALLOWED_EXTENSIONS, COEFFICIENTI_ASSENZE, COEFFICIENTI_VOTI, CONFERMA_CAMBIAMENTI_DATABASE, DOWNLOAD_DIRECTORY_PATH, EXCEL_PRE_MERGE_PATH, FRASI_PATH, LEGGI,  NOMI_CHECKBOX, RETURN_VALUE, SELECTORS, VERSION_PATH
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
from .database_funcs.ui_apis import costruisci_json_manage_data

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


@pagine_admin.route("/gestione_dati", 
    methods=["GET", "POST"]
)
@login_required
@admin_permission_required
def pagina_gestione_dati() -> Response | str:
    oggi=datetime.datetime.today().strftime('%Y-%m-%d') 
    elenco_classi = Classe.elenco_classi_studenti()
    return render_template(
    "manage_data.html",elenco_classi=elenco_classi,oggi=oggi)


@pagine_admin.route("/gestione_dati/stato", 
    methods=["GET", "POST"]
)
@login_required
@admin_permission_required
def invia_tabella() -> Response | str:
    nome_classe = request.args.get("classSelector")
    data = request.args.get("dateSelector")
    print(request.args)

    print(nome_classe)
    if not nome_classe :
        return "<p>Seleziona una classe classe</p>"
    if not data:
        data =      datetime.datetime.today().strftime('%Y-%m-%d') 

    stato=costruisci_json_manage_data(nome_classe,data)

    return render_template("templates/manage_data_table.html",stato=stato,nomi_checkbox=NOMI_CHECKBOX,nomi_selectors=SELECTORS)
@pagine_admin.route("/gestione_dati/checkbox",methods=["POST"])
@login_required
@admin_permission_required
def gestisci_checkbox():
    studente_id=0
    data_str=""
    checkbox={}
    for chiave,valore in request.form.items():
        if chiave == "uid":
            studente_id=int(valore)
        elif chiave == "dateSelector":
            data_str=valore
        else:
            checkbox={"nome":chiave,"valore":valore=="true"}
    studente = Utente.da_id(studente_id)
    stored_check=studente.cronologia_studente.filter_by(data=data_str,attivita=checkbox["nome"]).first()
    if stored_check:
        if not checkbox["valore"]:
            db.session.delete(stored_check)
    else:
        if checkbox["valore"]:
            db.session.add(Cronologia(
                attivita=checkbox["nome"],
                modifica_punti=NOMI_CHECKBOX[checkbox["nome"]],
                data=data_str,
                stagione=Info.ottieni_ultima_stagione(),# TODO : MODIFICARE CON VERA STAGIONE
                utente_id=studente_id,
                ))
    db.session.commit()

    return '',204
@pagine_admin.route("/gestione_dati/selector",methods=["POST"])
@login_required
@admin_permission_required
def gestisci_selector():
    studente_id=0
    data_str=""
    selector={}
    for chiave,valore in request.form.items():
        if chiave == "uid":
            studente_id=int(valore)
        elif chiave == "dateSelector":
            data_str=valore
        else:
            selector={"nome":chiave,"valore":valore}
    studente = Utente.da_id(studente_id)
    stored_selector=studente.cronologia_studente.filter_by(data=data_str,attivita=selector["nome"]).first()
    if stored_check:
        if selector["valore"]=="Presente":
            db.session.delete(stored_check)
    else:
        if selector["valore"]:
            db.session.add(Cronologia(
                attivita=selector["nome"],
                modifica_punti=NOMI_CHECKBOX[selector["nome"]],
                data=data_str,
                stagione=Info.ottieni_ultima_stagione(),# TODO : MODIFICARE CON VERA STAGIONE
                utente_id=studente_id,
                ))
    db.session.commit()

    return '',204





