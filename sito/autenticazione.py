from pathlib import Path
from flask import (
    Blueprint,
    Response,
    render_template,
    request,
    flash,
)

from sito.errors_utils import admin_permission_required
from sito.errors_utils.errors_classes.users_error_classes import (
    FailedSignUpError,
    FailedLoginError,
)
from sito.pagine_sito import VUOTO
from . import db, app
import sito.misc_utils_funcs as mc_utils
import sito.auth_funcs as auth_utils
import sito.errors_utils as e_utils
from sito.errors_utils import InitPasswordNotSetError

with app.app_context():
    import sito.database_funcs as db_funcs
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import os

autenticazione = Blueprint("autenticazione", __name__)
SECRET_PASSWORD_PATH = os.path.join(
    Path.cwd(), "secrets", "secret_starter_admin_password.txt"
)


@autenticazione.route("/init_starter_admin")
def pagina_init_admin_starter() -> Response:
    with open(SECRET_PASSWORD_PATH) as f:
        starter_admin_password = f.read().strip()
    if starter_admin_password == VUOTO:
        raise InitPasswordNotSetError(
            "Non hai cambiato la passoword vuota di default di admin starter"
        )
    try:
        auth_utils.crea_admin_user(
            email="s-admin.starter@isiskeynes.it",
            account_attivo=1,
            nominativo="starter admin",
            password=starter_admin_password,
        )
    except FailedSignUpError:
        pass
    os.remove(SECRET_PASSWORD_PATH)
    return e_utils.redirect_home()


@autenticazione.route("/login", methods=["GET", "POST"])
def pagina_login() -> str | Response:
    if request.method == "POST":
        dati = request.form
        email = dati.get("email")
        password = dati.get("password")
        try:
            auth_utils.login(email, password)
            return e_utils.redirect_home()
        except FailedLoginError as error_message:
            flash(
                str(error_message),
                category="error",
            )
    return render_template("login.html", user=current_user)


@autenticazione.route("/sign_up", methods=["GET", "POST"])
def pagina_sign_up() -> str | Response:
    if request.method == "POST":
        dati = request.form

        email = dati.get("email").strip().lower()
        nominativo = dati.get("nominativo").strip()
        password = dati.get("password")
        password_di_conferma = dati.get("password_di_conferma")
        nominativo = mc_utils.capitalize_all(nominativo)
        user = db_funcs.user_da_nominativo(nominativo)
        if db_funcs.user_da_email(email) and user.account_attivo:
            flash(
                "Esiste già un altro account con questa email in uso", category="error"
            )
        elif "'" in email:
            flash("L'email non può contenere apici", category="error")
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
            user.password = generate_password_hash(password, method="pbkdf2:sha256")
            user.email = email
            user.account_attivo = 1
            db.session.commit()

            flash("Account creato con successo!", category="success")
            login_user(user, remember=True)
            return e_utils.redirect_home()

    return render_template(
        "sign_up.html", user=current_user, studenti=db_funcs.elenco_studenti()
    )


@autenticazione.route("/crea_admin", methods=["GET", "POST"])
@login_required
@admin_permission_required
def pagina_crea_admin() -> str | Response:
    if request.method == "POST":
        dati = request.form
        email = dati.get("email").lower()
        nome = dati.get("nome").capitalize()
        cognome = dati.get("cognome").capitalize()
        password = dati.get("password")
        password_di_conferma = dati.get("password_di_conferma")

        nominativo = f"{cognome} {nome}"

        if len(password) < 5:
            flash("La password deve essere almeno di 5 caratteri", category="error")
        elif password != password_di_conferma:
            flash("La password di conferma non e' corretta", category="error")
        try:
            auth_utils.crea_admin_user(
                email=email,
                nominativo=nominativo,
                password=password,
                account_attivo=1,
            )
            return e_utils.redirect_home()
        except FailedSignUpError as error_message:
            flash(str(error_message), category="error")

    return render_template("crea_admin.html", user=current_user)


@autenticazione.route("/logout")
@login_required
def pagina_logout() -> Response:
    logout_user()
    return e_utils.redirect_home()
