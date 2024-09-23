from flask import Blueprint, render_template, request, redirect, url_for, flash
from sito.database_funcs.cronology_utils_funcs import cronologia_utente
from sito.misc_utils_funcs.permission_utils import errore_accesso
from . import db, app

with app.app_context():
    import sito.database_funcs as db_funcs
import sito.misc_utils_funcs as mc_utils
import sito.chart_funcs as ct_funcs

from flask_login import login_required, current_user
from .modelli import Classi, Info, Cronologia
from os import path
from .refactor import refactor_file
from pathlib import Path

pagine_sito = Blueprint("pagine_sito", __name__)
FILE_ERRORE = path.join(Path.cwd(), "data", "errore.txt")
FILE_VERSIONI = path.join(Path.cwd(), "versioni.txt")
LEGGI = "r"
RETURN_VALUE = "bottone"
ELIMINA_UTENTE = "elimina"
AGGIUNGI_CLASSE = "nuova"
ENTRA_NELLA_CLASSE = "raggiunti"
CONFERMA_CAMBIAMENTI_DATABASE = "load_database"
VUOTO = ""


ALLOWED_EXTENSIONS = set(["xlsx"])

from functools import wraps


def admin_permission_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if the current_user has account_attivo == 1
        if not current_user.admin_user:
            return errore_accesso()
        return func(*args, **kwargs)

    return decorated_function


@pagine_sito.route("/")
def home():
    classe_name = None
    if current_user.is_authenticated:
        classe_name = db_funcs.classe_da_id(current_user.classe_id).classe
    return render_template("home.html", user=current_user, classe_name=classe_name)


@pagine_sito.route("/classe/<classe_name>", methods=["GET", "POST"])
@login_required
def classe(classe_name):
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
        classe=classe.classe,
        studenti=studenti,
        n_stagioni=n_stagioni,
        stagione_corrente=stagione_corrente,
        cronologia_da_user=db_funcs.cronologia_da_user,
        list_label=ct_funcs.list_label,
        list_data=ct_funcs.list_data,
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
        list_attivita=ct_funcs.list_attivita,
        zip=zip,
    )


@pagine_sito.route("/classe/<classe_name>/<nominativo>/<int:stagione>", methods=["GET"])
@login_required
def info_studente(classe_name, nominativo, stagione):
    nominativo = " ".join(nominativo.split("_"))
    if current_user.nominativo != nominativo and not current_user.admin_user:
        return errore_accesso()
    return render_template(
        "info_studente.html",
        user=current_user,
        stagione_corrente=stagione,
        studente=db_funcs.user_da_nominativo(nominativo),
        cronologia_da_user=db_funcs.cronologia_da_user,
        list_label=ct_funcs.list_label,
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
        list_data=ct_funcs.list_data,
        list_attivita=ct_funcs.list_attivita,
        cronologia_stagione=cronologia_utente,
        zip=zip,
        classe=classe_name,
    )


@pagine_sito.route("/regole")
def regole():
    classe_name = None
    if current_user.is_authenticated:
        classe_name = db_funcs.classe_da_id(current_user.classe_id).classe
    return render_template("regole.html", user=current_user, classe_name=classe_name)


@pagine_sito.route("/admin_dashboard")
@login_required
@admin_permission_required
def admin_dashboard():
    errori = open(path.join(Path.cwd(), "data", "errore.txt"), "r").read() == VUOTO
    numero_degli_studenti = len(db_funcs.elenco_studenti())
    numero_delle_classi = len(db_funcs.elenco_classi_studenti())
    numero_degli_admin = len(db_funcs.elenco_admin())
    numero_studenti_registrati = len(db_funcs.elenco_studenti_registrati())
    if not db_funcs.get_last_season():
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
def menu_classi():
    classi = db_funcs.elenco_classi_studenti()
    error_file = path.join(Path.cwd(), "data", "errore.txt")

    if request.method == "POST":
        dati = request.form
        if dati[RETURN_VALUE] == CONFERMA_CAMBIAMENTI_DATABASE:
            file = request.files["file_db"]
            if mc_utils.allowed_files(file.filename):
                new_filename = "foglio.xlsx"

                save_location = path.join(path.join(Path.cwd(), "data"), new_filename)
                file.save(save_location)
                error_file = path.join(Path.cwd(), "data", "errore.txt")
                with open(error_file, "w") as f:
                    f.write(VUOTO)
                refactor_file(current_user)

                classi = db_funcs.elenco_classi_studenti()

            else:
                with open(error_file, "w") as f:
                    f.write(
                        f"Impossibile aprire questa estensione dei file, per adesso puoi caricare il database sono in questo/i formato/i : {ALLOWED_EXTENSIONS}"
                    )
    with open(error_file, LEGGI) as f:
        error = f.read() != VUOTO

    return render_template("menu_classi.html", classi=classi, error=error)


@pagine_sito.route("/db_errori")
@login_required
@admin_permission_required
def db_errori():
    with open(FILE_ERRORE, LEGGI) as file_errore:
        content_error = file_errore.read().splitlines()
    return "<br><br>".join(content_error)


@pagine_sito.route("/versioni")
@login_required
@admin_permission_required
def versioni():
    return "<br>".join(reversed(open(FILE_VERSIONI, LEGGI).read().splitlines()))


@pagine_sito.route(
    "/classe/<classe_name>/<studente_id>/<stagione>/create_event", methods=["POST"]
)
@login_required
@admin_permission_required
def create_event(classe_name, studente_id, stagione):
    # Recupera i dati dal form di creazione evento
    data = request.form["data"]
    attivita = request.form["attivita"]
    modifica_punti = request.form["modifica_punti"]
    stagione = request.form["stagione"]

    # Crea un nuovo evento
    nuovo_evento = Cronologia(
        utente_id=studente_id,
        stagione=stagione,
        data=data,
        attivita=attivita,
        modifica_punti=modifica_punti,
        punti_cumulativi=0,
    )

    # Aggiungi l'evento al database
    db.session.add(nuovo_evento)
    db.session.commit()
    db_funcs.aggiorna_punti_cumulativi(db_funcs.user_da_id(studente_id))
    db_funcs.aggiorna_punti(db_funcs.user_da_id(studente_id))

    # Reindirizza alla pagina della classifica
    return redirect(
        url_for(
            "pagine_sito.info_studente",
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
def delete_event(classe_name, studente_id, stagione, event_id):
    # Recupera l'evento da eliminare
    evento = db_funcs.evento_da_id(event_id)

    if evento:
        db_funcs.elimina_evento_cronologia(evento)

        db_funcs.aggiorna_punti_cumulativi(db_funcs.user_da_id(studente_id))
        db_funcs.aggiorna_punti(db_funcs.user_da_id(studente_id))
        flash("Evento eliminato con successo", "success")
    else:
        flash("Evento non trovato", "error")

    # Reindirizza alla pagina della classifica
    return redirect(
        url_for(
            "pagine_sito.info_studente",
            classe_name=classe_name,
            nominativo="_".join(db_funcs.user_da_id(studente_id).nominativo.split()),
            stagione=stagione,
        )
    )


@pagine_sito.route("/elenco_user/<elenco_type>", methods=["GET"])
@login_required
@admin_permission_required
def elenco_user_display(elenco_type):
    if elenco_type == "tutti_gli_studenti_registrati":

        utenti = db_funcs.elenco_studenti_registrati()
    elif elenco_type == "tutti_gli_admin":
        utenti = db_funcs.elenco_admin()
    else:

        utenti = db_funcs.elenco_studenti()
    return render_template(
        "elenco_user.html", utenti=utenti, classe_da_id=db_funcs.classe_da_id
    )
