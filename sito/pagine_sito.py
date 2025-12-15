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
from sito.costanti import COEFFICIENTI_VOTI
from sito.database_funcs import list_database_elements
import sito.errors_utils as e_utils
from sito.errors_utils.errors_classes.data_error_classes import InvalidSeasonError
from sito.misc_utils_funcs import parse_utils
from sito.misc_utils_funcs.misc_utils import query_json_by_nominativo_and_date
from . import db, app

with app.app_context():
    import sito.database_funcs as db_funcs
import sito.misc_utils_funcs as mc_utils
import sito.chart_funcs as ct_funcs
import sito.excel_funcs as xlsx_funcs

from sito.errors_utils import admin_permission_required


from flask_login import login_required, current_user
from .modelli import Info, Cronologia
from os import path, listdir
from .load_data import load_data, merge_excel

from pathlib import Path
import datetime
import json
from math import ceil, sqrt

pagine_sito = Blueprint("pagine_sito", __name__)
FILE_ERRORE = path.join(Path.cwd(), "data", "errore.txt")
FILE_VERSIONI = path.join(Path.cwd(), "versioni.txt")
FILE_LOG = path.join(Path.cwd(), "data", "log.txt")
PATH_CARTELLA_LOGHI = path.join(Path.cwd(), "sito", "static", "images", "loghi")
FRASI_PATH = path.join(Path.cwd(), "data", "frasi.json")

GLOBAL_DATA = path.join(Path.cwd(), "data", "global_data.json")


SAVE_LOCATION_PATH = path.join(path.join(Path.cwd(), "data"), "foglio_pre-merge.xlsx")
DOWNLOAD_PATH = path.join(Path.cwd(), "data")
LEGGI = "r"
RETURN_VALUE = "bottone"
ELIMINA_UTENTE = "elimina"
AGGIUNGI_CLASSE = "nuova"
ENTRA_NELLA_CLASSE = "raggiunti"
CONFERMA_CAMBIAMENTI_DATABASE = "load_database"
VUOTO = ""


ALLOWED_EXTENSIONS = set(["xlsx"])


@pagine_sito.route("/")
def pagina_home() -> str:
    classe_name = None
    if current_user.is_authenticated:
        classe_name = db_funcs.classe_da_id(current_user.classe_id).classe
    loghi = [logo for logo in listdir(PATH_CARTELLA_LOGHI)]
    lenght_square_of_loghi = ceil(sqrt(len(loghi)))
    frase = mc_utils.get_random_json_item(FRASI_PATH)
    last_season = list_database_elements.get_last_season()
    return render_template(
        "home.html",
        user=current_user,
        classe_name=classe_name,
        lista_loghi=loghi,
        lenght_square_of_loghi=lenght_square_of_loghi,
        frase=frase,
        last_season=last_season,
    )


@pagine_sito.route("/classe/<classe_name>/<int:stagione>", methods=["GET", "POST"])
@login_required
def pagina_classe(
    classe_name: str,
    stagione: int,
) -> str:
    if current_user.admin_user:
        classe = db_funcs.classe_da_nome(classe_name)
    else:
        classe = db_funcs.classe_da_id(current_user.classe_id)
    studenti = db_funcs.classifica_studenti_di_una_classe(stagione, classe)
    n_stagioni = db_funcs.get_last_season()
    loghi = {logo.rsplit(".", 1)[0]: logo for logo in listdir(PATH_CARTELLA_LOGHI)}
    return render_template(
        "classe.html",
        user=current_user,
        classe=classe,
        studenti=studenti,
        n_stagioni=n_stagioni,
        stagione_corrente=stagione,
        get_season_points=parse_utils.get_season_points,
        cronologia_da_user=db_funcs.cronologia_user,
        elenco_date=ct_funcs.elenco_date,
        elenco_punti_cumulativi=ct_funcs.elenco_punti_cumulativi,
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
        zip=zip,
        url_name=mc_utils.insert_underscore_name,
        classifica_squadre=db_funcs.classifica_squadre,
        loghi=loghi,
    )


@pagine_sito.route(
    "/classe/<classe_name>/<int:stagione>/<nominativo_con_underscore>",
    methods=["GET"],
)
@login_required
def pagina_info_studente(
    classe_name: str,
    stagione: int,
    nominativo_con_underscore: str,
) -> str | Response:
    if (
        mc_utils.insert_underscore_name(current_user.nominativo)
        != nominativo_con_underscore
        and not current_user.admin_user
    ):
        return e_utils.redirect_home()
    nominativo = mc_utils.remove_underscore_name(nominativo_con_underscore)
    loghi = {logo.rsplit(".", 1)[0]: logo for logo in listdir(PATH_CARTELLA_LOGHI)}
    return render_template(
        "info_studente.html",
        user=current_user,
        stagione_corrente=stagione,
        studente=db_funcs.user_da_nominativo(nominativo),
        cronologia_da_user=db_funcs.cronologia_user,
        elenco_date=ct_funcs.elenco_date,
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
        elenco_punti_cumulativi=ct_funcs.elenco_punti_cumulativi,
        elenco_attivita=ct_funcs.elenco_attivita,
        cronologia_stagione=db_funcs.cronologia_user_di_una_stagione,
        zip=zip,
        classe=classe_name,
        loghi=loghi,
    )


@pagine_sito.route("/regole")
def pagina_regole() -> str:
    classe_name = None
    if current_user.is_authenticated:
        classe_name = db_funcs.classe_da_id(current_user.classe_id).classe
    return render_template("regole.html", user=current_user, classe_name=classe_name)


@pagine_sito.route("/coming_soon")
def pagina_comingsoon() -> str:
    classe_name = None
    if current_user.is_authenticated:
        classe_name = db_funcs.classe_da_id(current_user.classe_id).classe
    return render_template(
        "coming_soon.html", user=current_user, classe_name=classe_name
    )


@pagine_sito.route("/admin_dashboard")
@login_required
@admin_permission_required
def pagina_admin_dashboard() -> str:
    errori = not mc_utils.is_empty(FILE_ERRORE)
    numero_degli_studenti = len(db_funcs.elenco_studenti())
    numero_delle_classi = len(db_funcs.elenco_classi_studenti())
    numero_degli_admin = len(db_funcs.elenco_admin())
    numero_studenti_registrati = len(db_funcs.elenco_studenti_registrati())
    numero_studenti_non_registrati = len(db_funcs.elenco_studenti_non_registrati())

    if not Info.query.filter_by().first():
        db.session.add(Info(last_season=0))
        db.session.commit()
    return render_template(
        "admin_dashboard.html",
        numero_studenti=numero_degli_studenti,
        numero_classi=numero_delle_classi,
        numero_admin=numero_degli_admin,
        numero_studenti_registrati=numero_studenti_registrati,
        numero_studenti_non_registrati=numero_studenti_non_registrati,
        novita=db_funcs.classifica_studenti(db_funcs.get_last_season())[0:8],
        errori=errori,
        classe_da_id=db_funcs.classe_da_id,
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
        get_season_points=parse_utils.get_season_points,
        last_season=list_database_elements.get_last_season(),
    )


@pagine_sito.route("/classi", methods=["GET"])
@login_required
@admin_permission_required
def pagina_menu_classi() -> str:
    classi = db_funcs.elenco_classi_studenti()
    last_season = list_database_elements.get_last_season()
    return render_template("menu_classi.html", classi=classi, last_season=last_season)


@pagine_sito.route("/db_errori")
@login_required
@admin_permission_required
def pagina_db_errori() -> str:
    with open(FILE_ERRORE, LEGGI) as file_errore:
        content_error = file_errore.read().splitlines()
    return "<br><br>".join(content_error)


@pagine_sito.route("/versioni")
@login_required
@admin_permission_required
def pagina_versioni() -> str:
    return "<br>".join(reversed(open(FILE_VERSIONI, LEGGI).read().splitlines()))


@pagine_sito.route(
    "/classe/<classe_name>/<studente_id>/<int:stagione>/create_event", methods=["POST"]
)
@login_required
@admin_permission_required
def pagina_create_event(classe_name: str, studente_id: int, stagione: int) -> Response:
    data = request.form["data"]
    attivita = request.form["attivita"]
    modifica_punti = request.form["modifica_punti"]
    stagione = float(request.form["stagione"])

    if stagione > db_funcs.get_last_season():
        raise InvalidSeasonError("La season che hai inserito non esiste")
    xlsx_funcs.aggiungi_riga_excel(
        data,
        stagione,
        classe_name,
        db_funcs.user_da_id(studente_id).nominativo,
        attivita,
        modifica_punti,
    )
    nuovo_evento = Cronologia(
        utente_id=studente_id,
        stagione=stagione,
        data=data,
        attivita=attivita,
        modifica_punti=modifica_punti,
        punti_cumulativi=0,
    )

    db.session.add(nuovo_evento)
    db.session.commit()

    db_funcs.aggiorna_punti_composto(db_funcs.user_da_id(studente_id))

    mc_utils.set_item_of_json(
        GLOBAL_DATA, "ultima_modifica", str(datetime.datetime.now().date())
    )
    return redirect(
        url_for(
            "pagine_sito.pagina_info_studente",
            classe_name=classe_name,
            nominativo_con_underscore="_".join(
                db_funcs.user_da_id(studente_id).nominativo.split()
            ),
            stagione=stagione,
        )
    )


@pagine_sito.route(
    "/classe/<classe_name>/<studente_id>/<stagione>/delete_event/<int:event_id>",
    methods=["POST"],
)
@login_required
@admin_permission_required
def pagina_delete_event(
    classe_name: str, studente_id: int, stagione: int, event_id: int
) -> Response:
    evento = db_funcs.evento_da_id(event_id)
    xlsx_funcs.elimina_riga_excel(
        evento.data,
        evento.stagione,
        classe_name,
        db_funcs.user_da_id(studente_id).nominativo,
        evento.attivita,
        evento.modifica_punti,
    )
    if evento:
        db_funcs.elimina_evento_cronologia(evento)

        db_funcs.aggiorna_punti_composto(db_funcs.user_da_id(studente_id))

        mc_utils.set_item_of_json(
            GLOBAL_DATA, "ultima_modifica", str(datetime.datetime.now().date())
        )
        flash("Evento eliminato con successo", "success")
    else:
        flash("Evento non trovato", "error")

    return redirect(
        url_for(
            "pagine_sito.pagina_info_studente",
            classe_name=classe_name,
            nominativo_con_underscore=mc_utils.insert_underscore_name(
                db_funcs.user_da_id(studente_id).nominativo
            ),
            stagione=stagione,
        )
    )


@pagine_sito.route("/elenco_user/<elenco_type>", methods=["GET"])
@login_required
@admin_permission_required
def pagina_elenco_user_display(elenco_type: str) -> str:
    if elenco_type == "tutti_gli_studenti_registrati":
        utenti = db_funcs.elenco_studenti_registrati()

    elif elenco_type == "studenti_non_registrati":
        utenti = db_funcs.elenco_studenti_non_registrati()

    elif elenco_type == "tutti_gli_admin":
        utenti = db_funcs.elenco_admin()
    else:
        utenti = db_funcs.elenco_studenti()
    return render_template(
        "elenco_user.html", utenti=utenti, classe_da_id=db_funcs.classe_da_id
    )


@pagine_sito.route("/gestione_dati/<classe_name>/", 
    methods=["GET", "POST"]
)
@login_required
@admin_permission_required
def pagina_gestione_dati_r(classe_name:str) -> str:
    return redirect(url_for("pagine_sito.pagina_gestione_dati",classe_name=classe_name,data_str='none'))

@pagine_sito.route("/gestione_dati/<classe_name>/<data_str>", 
    methods=["GET", "POST"]
)
@login_required
@admin_permission_required
def pagina_gestione_dati(classe_name:str,data_str:str) -> str:
    data_str = datetime.datetime.today().strftime('%Y-%m-%d') if not data_str else data_str
    elenco_classi =[x.classe for x in list_database_elements.elenco_classi_studenti()]
    if request.method == "POST":
        returned_form = request.form
        form_id = returned_form.get("form_id")
        if form_id == "classSelector":
            classe_name = returned_form.get("classSelector")
            return redirect(url_for("pagine_sito.pagina_gestione_dati",classe_name=classe_name,data_str=data_str))
        elif form_id == "dateSelector":
            data_str = returned_form.get("dateSelector")

            return redirect(url_for("pagine_sito.pagina_gestione_dati",classe_name=classe_name,data_str=data_str))

        elif form_id == "students_data":
            valori_ritornati={str(x.id):{"USER":x} for x in db_funcs.studenti_da_classe(db_funcs.classe_da_nome(classe_name))}

            for identificativo,valore in returned_form.items():
                if identificativo == "form_id": continue
                print(identificativo)
                Uid,tipo=identificativo.split('_')
                valori_ritornati[Uid][tipo] = valore
            for Uid,value_dict in valori_ritornati.items():
                user = value_dict["USER"]
                eventi_da_eliminare = [
                    evento
                    for evento in user.cronologia_studente
                    if evento.data == data_str
                ]

                for evento in eventi_da_eliminare:
                    db.session.delete(evento)







                #RICHIAMA IL RICALCOLO DEI PUNTI DOPO PLS

                db.session.commit()





                

        else:
            print("you alone in this one lil blud")
    if classe_name=="admin":
        classe_name="none"
    if classe_name != "none":
        lista_studenti_v=[[x,dict()] for x in db_funcs.studenti_da_classe(db_funcs.classe_da_nome(classe_name))]
        lista_studenti_v.sort(key=lambda x: x[0].nominativo)

        if Cronologia.query.filter_by(data=data_str).first() is not None:
            for ind,(studente,_) in enumerate(lista_studenti_v):
                frase = query_json_by_nominativo_and_date(studente.nominativo,data_str)
                if frase is not None:
                    lista_studenti_v[ind][1]["frase"]=frase
                cron = filter(lambda x: x.data==data_str,studente.cronologia_studente)
                for evento in cron:
                    v = 1
                    if evento.attivita in COEFFICIENTI_VOTI:
                        v = evento.modifica_punti/COEFFICIENTI_VOTI[evento.attivita]
                        lista_studenti_v[ind][1]['Voto']=v
                    lista_studenti_v[ind][1][evento.attivita]=v
    else:
        lista_studenti_v=None

    return render_template(
    "manage_data.html",classe_name=classe_name,elenco_classi=elenco_classi,data=data_str,lista_studenti_v=lista_studenti_v
     )





@pagine_sito.route("/load_db", methods=["POST"])
@login_required
@admin_permission_required
def pagina_load_db() -> Response:
    if request.method == "POST":
        dati = request.form
        if dati[RETURN_VALUE] == CONFERMA_CAMBIAMENTI_DATABASE:
            file = request.files["file_db"]
            if not mc_utils.allowed_files(file.filename):
                with open(FILE_ERRORE, "w") as f:
                    f.write(
                        f"Impossibile aprire questa estensione dei file, per adesso puoi caricare il database sono in questo/i formato/i : {ALLOWED_EXTENSIONS}"
                    )

                return redirect(url_for("pagine_sito.pagina_gestione_dati"))
            file.save(SAVE_LOCATION_PATH)
            merge_excel()
            load_data(current_user)

    return redirect(url_for("pagine_sito.pagina_gestione_dati"))


@app.route("/download/<filename>")
@login_required
@admin_permission_required
def download_file(filename):
    return send_from_directory(DOWNLOAD_PATH, filename, as_attachment=True)


@app.route("/log_excel")
@login_required
@admin_permission_required
def pagina_log_excel():
    return "<br>".join(reversed(open(FILE_LOG, LEGGI).read().splitlines()))


@pagine_sito.route("/aggiunta_frase", methods=["POST"])
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
    return redirect(url_for("pagine_sito.pagina_gestione_dati"))
