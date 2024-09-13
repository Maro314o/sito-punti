from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from flask_login import login_required, current_user
from .modelli import User, Classi, Info
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from os import path, remove
from .refactor import refactor_file

from pathlib import Path

pagine_sito = Blueprint("pagine_sito", __name__)
ALLOWED_EXTENSIONS = set(["xlsx"])
FILE_ERRORE = path.join(Path.cwd(), "instance", "errore.txt")
FILE_VERSIONI = path.join(Path.cwd(), "instance", "versioni.txt")
LEGGI = "r"
RETURN_VALUE = "bottone"
ELIMINA_UTENTE = "elimina"
AGGIUNGI_CLASSE = "nuova"
ENTRA_NELLA_CLASSE = "raggiunti"
CONFERMA_CAMBIAMENTI_DATABASE = "datab"
VUOTO = ""


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def cronologia_da_user(utente):
    return utente.cronologia_studente


def user_da_nominativo(nominativo):
    return User.query.filter_by(nominativo=nominativo).first()


def user_da_id(id):
    return User.query.filter_by(id=id).first()


def user_da_email(email):
    return User.query.filter_by(email=email).first()


def classe_da_nome(classe_name):
    return Classi.query.filter_by(classe=classe_name).first()


def classe_da_id(classe_id):
    return Classi.query.filter_by(id=classe_id).first()


def ordina_studenti_in_modo_decrescente(classe, stagione):
    return sorted(
        classe.studenti,
        key=lambda studente: float(studente.punti.split(",")[stagione - 1]),
    )[::-1]


def elenco_utenti():
    return User.query.filter_by().all()


def elenco_studenti():
    return [utente for utente in User.query.filter_by().all() if not utente.admin_user]


def elenco_admin():
    return [utente for utente in User.query.filter_by().all() if utente.admin_user]


def elenco_classi():  # non si conta la classe degli admin
    return [
        classe for classe in Classi.query.filter_by().all() if classe.classe != "admin"
    ]


def classifica_degli_studenti(stagione):
    return sorted(
        elenco_studenti(),
        key=lambda studente: float(studente.punti.split(",")[stagione - 1]),
    )[::-1]


def elenco_di_tutte_le_classi():
    return Classi.query.filter_by().all()


def elenco_squadre():
    return set([x.squadra for x in elenco_studenti()])


def errore_accesso():
    return redirect(url_for("pagine_sito.home"))


def list_data(Cronologia, stagione):
    return [x.punti_cumulativi for x in Cronologia if x.stagione == stagione]


def list_label(Cronologia, stagione):
    return [x.data for x in Cronologia if x.stagione == stagione]


def list_attivita(Cronologia, stagione):
    return [x.attivita for x in Cronologia if x.stagione == stagione]


def calcola_valore_rgb(squadra):
    somma_ascii = sum(ord(char) ** 3 for char in squadra) + 70

    r = somma_ascii % 256
    g = (somma_ascii // 2) % 256
    b = (somma_ascii // 3) % 256

    return r, g, b, 0.3


@pagine_sito.route("/")
def home():
    try:
        return render_template(
            "home.html",
            user=current_user,
            classe_name=classe_da_id(current_user.classe_id).classe,
        )
    except:
        return render_template(
            "home.html", user=current_user, classe_name="Login_error"
        )


@pagine_sito.route("/classe/<classe_name>", methods=["GET", "POST"])
@login_required
def pag_classe(classe_name):
    stagione_corrente = Info.query.filter_by().all()[0].last_season
    if current_user.admin_user:
        classe = classe_da_nome(classe_name)
    else:
        classe = classe_da_id(current_user.classe_id)
    if request.method == "POST":
        dati = request.form
        if dati.get("selected_season"):
            stagione_corrente = int(dati.get("selected_season"))

    studenti = ordina_studenti_in_modo_decrescente(classe, stagione_corrente)
    n_stagioni = Info.query.filter_by().all()[0].last_season
    return render_template(
        "classe.html",
        user=current_user,
        classe=classe.classe,
        studenti=studenti,
        n_stagioni=n_stagioni,
        stagione_corrente=stagione_corrente,
        cronologia_da_user=cronologia_da_user,
        list_label=list_label,
        list_data=list_data,
        calcola_valore_rgb=calcola_valore_rgb,
        list_attivita=list_attivita,
        zip=zip,
    )


@pagine_sito.route("/classe/<classe_name>/<studente_id>/<stagione>", methods=["GET"])
@login_required
def info_studente(classe_name, studente_id, stagione):
    stagione = int(stagione) - 1
    return render_template(
        "info_studente.html",
        user=current_user,
        stagione_corrente=stagione,
        studente=user_da_id(studente_id),
        cronologia_da_user=cronologia_da_user,
        list_label=list_label,
        calcola_valore_rgb=calcola_valore_rgb,
        list_data=list_data,
        list_attivita=list_attivita,
        zip=zip,
    )


@pagine_sito.route("/regole")
def regole():
    try:
        return render_template(
            "regole.html",
            user=current_user,
            classe_name=classe_da_id(current_user.classe_id).classe,
        )
    except:
        return render_template(
            "regole.html", user=current_user, classe_name="Login_error"
        )


@pagine_sito.route("/admin_dashboard")
@login_required
def admin_dashboard():
    admin_user = current_user.admin_user
    errori = open(path.join(Path.cwd(), "instance", "errore.txt"), "r").read() == VUOTO
    if admin_user:
        numero_degli_studenti = len(elenco_studenti())
        numero_delle_classi = len(elenco_classi())
        numero_degli_admin = len(elenco_admin())
        numero_delle_squadre = len(elenco_squadre())
        return render_template(
            "admin_dashboard.html",
            numero_studenti=numero_degli_studenti,
            numero_classi=numero_delle_classi,
            numero_admin=numero_degli_admin,
            numero_squadre=numero_delle_squadre,
            novita=classifica_degli_studenti(
                Info.query.filter_by().all()[0].last_season
            )[0:8],
            errori=errori,
            classe_da_id=classe_da_id,
            calcola_valore_rgb=calcola_valore_rgb,
        )


@pagine_sito.route("/classi", methods=["GET", "POST"])
@login_required
def classi():
    if current_user.admin_user:
        error = 0
        classi = elenco_classi()
        error_file = path.join(Path.cwd(), "instance", "errore.txt")

        if request.method == "POST":
            dati = request.form
            if dati[RETURN_VALUE] == ENTRA_NELLA_CLASSE:
                classe_name = dati.get("classe")
                classe = classe_da_nome(classe_name)
                return redirect(
                    url_for("pagine_sito.classe", classe_name=classe.classe)
                )

            if dati[RETURN_VALUE] == AGGIUNGI_CLASSE:
                classe_name = dati.get("classe")
                if classe_name != VUOTO and classe_name not in [
                    x.classe for x in elenco_di_tutte_le_classi()
                ]:
                    db.session.add(Classi(classe=classe_name))
                    db.session.commit()

            if dati[RETURN_VALUE] == CONFERMA_CAMBIAMENTI_DATABASE:
                file = request.files["filen"]
                if allowed_file(file.filename):
                    new_filename = "foglio.xlsx"

                    save_location = path.join(
                        path.join(Path.cwd(), "instance"), new_filename
                    )
                    file.save(save_location)
                    error_file = path.join(Path.cwd(), "instance", "errore.txt")
                    with open(error_file, "w") as f:
                        f.write(VUOTO)
                    refactor_file()

                    classi = elenco_classi()

                else:
                    with open(error_file, "w") as f:
                        f.write(VUOTO)
                    with open(error_file, "w") as f:
                        f.write(
                            f"Impossibile aprire questa estensione dei file, per adesso puoi caricare il database sono in questo/i formato/i : {ALLOWED_EXTENSIONS}"
                        )
        with open(error_file, LEGGI) as f:
            if f.read() == VUOTO:
                error = 1

        return render_template("menu_classi.html", classi=classi, error=error)


@pagine_sito.route("/db_errori")
@login_required
def db_errori():
    if current_user.admin_user is False:
        return errore_accesso()
    with open(FILE_ERRORE, LEGGI) as file_errore:
        content_error = file_errore.read().splitlines()
    return "<br><br>".join(content_error)


@pagine_sito.route("/versioni")
def versioni():
    return "<br>".join(reversed(open(FILE_VERSIONI, LEGGI).read().splitlines()))
