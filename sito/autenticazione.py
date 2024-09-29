from pathlib import Path
from flask import (
    Blueprint,
    Response,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)

from sito.errors_utils import admin_permission_required
from sito.pagine_sito import VUOTO
from .modelli import User, Classi
from . import db, app
import sito.misc_utils_funcs as mc_utils

import sito.errors_utils as e_utils
from sito.errors_utils import InitPasswordNotSet

with app.app_context():
    import sito.database_funcs as db_funcs
import sito.misc_utils_funcs as mc_utils
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import os

autenticazione = Blueprint("autenticazione", __name__)


@autenticazione.route("/init_starter_admin")
def init_admin_starter() -> Response:
    with open(
        os.path.join(Path.cwd(), "secrets", "secret_starter_admin_password.txt")
    ) as f:
        starter_admin_password = f.read().strip()
    if starter_admin_password == VUOTO:
        raise InitPasswordNotSet(
            "Non hai cambiato la passoword vuota di default di admin starter"
        )
    try:

        db_funcs.crea_admin_user(
            email="s-admin.starter@isiskeynes.it",
            nominativo="starter admin",
            password=starter_admin_password,
        )
    except:
        pass
    return e_utils.redirect_home()


@autenticazione.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db_funcs.user_da_email(email)

        if not user:
            flash(
                "L'email non esiste,se hai un email con questo account considera riprovare a crearlo (ci sono stati cambiamenti ad alcuni account) ",
                category="error",
            )
        elif user.account_attivo == 0:

            flash(
                "Non puoi loggarti all'interno di questo account perche' non e' ancora stato attivato.Attivalo registrandoti con questa email",
                category="error",
            )
        elif not check_password_hash(user.password, password):
            flash("La password non e' corretta", category="error")
        else:
            login_user(user, remember=True)
            return redirect(url_for("pagine_sito.home"))
    return render_template("login.html", user=current_user)


@autenticazione.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("pagine_sito.home"))


@autenticazione.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        dati = request.form

        email = dati.get("email").strip().lower()
        nominativo = dati.get("nominativo").strip()
        password = dati.get("password")
        password_di_conferma = dati.get("password_di_conferma")
        nominativo = mc_utils.capitalize_all(nominativo)
        user = db_funcs.user_da_nominativo(nominativo)
        if user_da_email(email):
            flash(
                "Esiste già un altro account con questa email in uso", category="error"
            )
        elif "'" in email:
            flash("L'email non può contenere apici", category="error")
        elif mc_utils.campi_vuoti(dati):
            flash("Devi compilare tutti i campi", category="error")
        elif "@isiskeynes.it" != email[-14:]:
            flash("Il dominio dell' email é sbagliato", category="error")
        elif "s-" != email[:2]:
            flash("hai dimenticato di mettere 's-' nell' email", category="error")
        elif not user:
            flash(
                "Non hai selezionato l'opzione Cognome e Nome correttamente. Assicurati di selezionarne uno solo tra quelli proposti e di non inserire altre lettere/caratteri",
                category="error",
            )
        elif user.account_attivo:
            flash("Esiste gia' un account associato a questa persona", category="error")
        elif len(password) < 5:
            flash("La password deve essere almeno di 5 caratteri", category="error")
        elif password != password_di_conferma:
            flash("La password di conferma non e' corretta", category="error")
        else:
            user.password = generate_password_hash(password, method="sha256")
            user.email = email
            user.account_attivo = 1
            db.session.commit()

            flash("Account creato con successo!", category="success")
            login_user(user, remember=True)
            return redirect((url_for("pagine_sito.home")))

    return render_template(
        "sign_up.html", user=current_user, studenti=db_funcs.elenco_studenti()
    )


@autenticazione.route("/crea_admin", methods=["GET", "POST"])
@login_required
@admin_permission_required
def crea_admin():

    if request.method == "POST":
        dati = request.form

        email = dati.get("email").lower()
        nome = dati.get("nome").capitalize()
        cognome = dati.get("cognome").capitalize()
        password = dati.get("password")
        password_di_conferma = dati.get("password_di_conferma")

        user = db_funcs.user_da_email(email)
        nominativo = f"{cognome} {nome}"
        if mc_utils.campi_vuoti(dati) is True:
            flash("Devi compilare tutti i campi", category="error")
        elif user:
            flash("Esiste gia' un account con questa email", category="error")
        elif len(password) < 5:
            flash("La password deve essere almeno di 5 caratteri", category="error")
        elif password != password_di_conferma:
            flash("La password di conferma non e' corretta", category="error")
        else:
            nuovo_utente = User(
                email=email,
                nominativo=nominativo,
                password=generate_password_hash(password, method="sha256"),
                punti="0",
                account_attivo=1,
                admin_user=1,
                classe_id=Classi.query.filter_by(classe="admin").first().id,
            )
            db.session.add(nuovo_utente)

            db.session.commit()
            flash("Account creato con successo!", category="success")
            return redirect((url_for("pagine_sito.home")))
    return render_template("crea_admin.html", user=current_user)
