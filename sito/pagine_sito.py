from flask import (
    Blueprint,
    Response,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
import sito.errors_utils as e_utils
from sito.errors_utils.errors_classes.data_error_classes import InvalidSeasonError
from . import db, app

with app.app_context():
    import sito.database_funcs as db_funcs
import sito.misc_utils_funcs as mc_utils
import sito.chart_funcs as ct_funcs
from sito.errors_utils import admin_permission_required

from flask_login import login_required, current_user
from .modelli import Classi, Info, Cronologia
from os import path, listdir
from .refactor import load_data
from pathlib import Path
from math import ceil, sqrt

pagine_sito = Blueprint("pagine_sito", __name__)
FILE_ERRORE = path.join(Path.cwd(), "data", "errore.txt")
FILE_VERSIONI = path.join(Path.cwd(), "versioni.txt")
PATH_CARTELLA_LOGHI = path.join(Path.cwd(), "sito", "static", "images", "loghi")


SAVE_LOCATION_PATH = path.join(path.join(Path.cwd(), "data"), "foglio.xlsx")
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
    return render_template(
        "home.html",
        user=current_user,
        classe_name=classe_name,
        lista_loghi=loghi,
        lenght_square_of_loghi=lenght_square_of_loghi,
    )


@pagine_sito.route("/classe/<classe_name>", methods=["GET", "POST"])
@login_required
def pagina_classe(classe_name) -> str:
    stagione_corrente = db_funcs.get_last_season()
    if current_user.admin_user:
        classe = db_funcs.classe_da_nome(classe_name)
    else:
        classe = db_funcs.classe_da_id(current_user.classe_id)
    if request.method == "POST":
        dati = request.form
        if dati.get("selected_season"):
            stagione_corrente = int(dati.get("selected_season"))

    studenti = db_funcs.classifica_studenti_di_una_classe(stagione_corrente, classe)
    n_stagioni = db_funcs.get_last_season()

    return render_template(
        "classe.html",
        user=current_user,
        classe=classe,
        studenti=studenti,
        n_stagioni=n_stagioni,
        stagione_corrente=stagione_corrente,
        cronologia_da_user=db_funcs.cronologia_user,
        elenco_date=ct_funcs.elenco_date,
        elenco_punti_cumulativi=ct_funcs.elenco_punti_cumulativi,
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
        zip=zip,
        url_name=mc_utils.insert_underscore_name,
        classifica_squadre=db_funcs.classifica_squadre,
    )


@pagine_sito.route(
    "/classe/<classe_name>/<nominativo_con_underscore>/<int:stagione>", methods=["GET"]
)
@login_required
def pagina_info_studente(
    classe_name: str, nominativo_con_underscore: str, stagione: int
) -> str | Response:

    if (
        mc_utils.insert_underscore_name(current_user.nominativo)
        != nominativo_con_underscore
        and not current_user.admin_user
    ):
        return e_utils.redirect_home()
    nominativo = mc_utils.remove_underscore_name(nominativo_con_underscore)
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
    )


@pagine_sito.route("/regole")
def pagina_regole() -> str:
    classe_name = None
    if current_user.is_authenticated:
        classe_name = db_funcs.classe_da_id(current_user.classe_id).classe
    return render_template("regole.html", user=current_user, classe_name=classe_name)


@pagine_sito.route("/admin_dashboard")
@login_required
@admin_permission_required
def pagina_admin_dashboard() -> str:
    errori = not mc_utils.is_empty(FILE_ERRORE)
    numero_degli_studenti = len(db_funcs.elenco_studenti())
    numero_delle_classi = len(db_funcs.elenco_classi_studenti())
    numero_degli_admin = len(db_funcs.elenco_admin())
    numero_studenti_registrati = len(db_funcs.elenco_studenti_registrati())
    if not Info.query.filter_by().first():
        db.session.add(Info(last_season=0))
        db.session.commit()
    return render_template(
        "admin_dashboard.html",
        numero_studenti=numero_degli_studenti,
        numero_classi=numero_delle_classi,
        numero_admin=numero_degli_admin,
        numero_studenti_registrati=numero_studenti_registrati,
        novita=db_funcs.classifica_studenti(db_funcs.get_last_season())[0:8],
        errori=errori,
        classe_da_id=db_funcs.classe_da_id,
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
    )


@pagine_sito.route("/classi", methods=["GET", "POST"])
@login_required
@admin_permission_required
def pagina_menu_classi() -> str:

    if request.method == "POST":
        dati = request.form
        if dati[RETURN_VALUE] == CONFERMA_CAMBIAMENTI_DATABASE:
            file = request.files["file_db"]
            if not mc_utils.allowed_files(file.filename):
                with open(FILE_ERRORE, "w") as f:
                    f.write(
                        f"Impossibile aprire questa estensione dei file, per adesso puoi caricare il database sono in questo/i formato/i : {ALLOWED_EXTENSIONS}"
                    )
                return render_template("menu_classi.html", classi=classi, error=1)

            file.save(SAVE_LOCATION_PATH)
            load_data(current_user)

    classi = db_funcs.elenco_classi_studenti()
    error = not mc_utils.is_empty(FILE_ERRORE)

    return render_template("menu_classi.html", classi=classi, error=error)


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
    db_funcs.aggiorna_punti_cumulativi(db_funcs.user_da_id(studente_id))
    db_funcs.aggiorna_punti(db_funcs.user_da_id(studente_id))

    return redirect(
        url_for(
            "pagine_sito.pagina_info_studente",
            classe_name=classe_name,
            nominativo="_".join(db_funcs.user_da_id(studente_id).nominativo.split()),
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

    if evento:
        db_funcs.elimina_evento_cronologia(evento)

        db_funcs.aggiorna_punti_cumulativi(db_funcs.user_da_id(studente_id))
        db_funcs.aggiorna_punti(db_funcs.user_da_id(studente_id))
        flash("Evento eliminato con successo", "success")
    else:
        flash("Evento non trovato", "error")

    return redirect(
        url_for(
            "pagine_sito.pagina_info_studente",
            classe_name=classe_name,
            nominativo=mc_utils.insert_underscore_name(
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
    elif elenco_type == "tutti_gli_admin":
        utenti = db_funcs.elenco_admin()
    else:

        utenti = db_funcs.elenco_studenti()
    return render_template(
        "elenco_user.html", utenti=utenti, classe_da_id=db_funcs.classe_da_id
    )
