from flask import Blueprint, render_template, request, flash, redirect, url_for
from .modelli import User, Classi
from . import db
from .pagine_sito import elenco_classi, elenco_di_tutte_le_classi, classe_da_nome, user_da_email, elenco_admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

autenticazione = Blueprint('autenticazione', __name__)


def campi_vuoti(dati):
    for campo in dati.values():
        if campo == '':
            return True
    return False


def crea_classe():
    return [classe.classe for classe in elenco_classi()]


@autenticazione.route('/login', methods=['GET', 'POST'])
def login():
    if len(elenco_di_tutte_le_classi()) == 0:
        db.session.add(Classi(classe='admin'))
        nuovo_utente = User(email="s-admin.starter@isiskeynes.it", nome='admin', cognome="starter",
                            password=generate_password_hash('highsecureadminpassword', method='sha256'), punti=0,
                            admin_user=1,account_attivo=1, classe_id=classe_da_nome('admin').id)
        db.session.add(nuovo_utente)
        db.session.commit()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = user_da_email(email)
        if not user:
            flash("L'email non esiste", category='error')
        elif not check_password_hash(user.password, password):
            flash("La password non e' corretta", category='error')
        else:

            login_user(user, remember=True)
            return redirect(url_for('pagine_sito.home'))
    return render_template("login.html", user=current_user)


@autenticazione.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('pagine_sito.home'))


@autenticazione.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    lista_classi = crea_classe()
    if request.method == 'POST':

        dati = request.form

        email = dati.get('email').lower()
        nome = dati.get('nome').lower()
        cognome = dati.get('cognome').lower()
        password = dati.get('password')
        password_di_conferma = dati.get('password_di_conferma')
        nome_classe = dati.get('classe')

        classe = classe_da_nome(nome_classe)

        user = user_da_email(email)

        if campi_vuoti(dati) is True:
            flash('Devi compilare tutti i campi', category='error')
        elif '@isiskeynes.it' not in email:
            flash('Il dominio dell\' email é sbagliato', category='error')
        elif 's-' not in email:
            flash('hai dimenticato di mettere \'s-\' nell\' email', category='error')
        elif email != f's-{cognome}.{nome}@isiskeynes.it':
            flash('L\'email non corrisponde con il nome e cognome', category='error')
        elif not user:
             flash("Non esiste uno studente con questa email")
        elif user.account_attivo:
            flash('Esiste gia\' un account con questa email', category='error')


        elif classe is None:
            flash('Seleziona una classe', category='error')
        elif len(password) < 5:
            flash('La password deve essere almeno di 5 caratteri', category='error')
        elif password != password_di_conferma:
            flash('La password di conferma non e\' corretta', category='error')
        else:
            user.account_attivo=1
            user.password=generate_password_hash(password, method='sha256')
            db.session.commit()

            flash('Account creato con successo!', category='success')
            login_user(user, remember=True)
            return redirect((url_for('pagine_sito.home')))

    return render_template("sign_up.html", user=current_user, lista_classi=lista_classi)


@autenticazione.route("/crea_admin", methods=["GET", "POST"])
@login_required
def crea_admin():
    if current_user.admin_user:
        if request.method == 'POST':

            dati = request.form

            email = dati.get('email').lower()
            nome = dati.get('nome').capitalize()
            cognome = dati.get('cognome').capitalize()
            password = dati.get('password')
            password_di_conferma = dati.get('password_di_conferma')

            user = user_da_email(email)

            if campi_vuoti(dati) is True:
                flash('Devi compilare tutti i campi', category='error')
            elif user:
                flash('Esiste gia\' un account con questa email', category='error')
            elif '@isiskeynes.it' not in email:
                flash('Il dominio dell\' email é sbagliato', category='error')
            elif 's-' not in email:
                flash('hai dimenticato di mettere \'s-\' nell\' email', category='error')
            elif email != f's-{cognome.lower()}.{nome.lower()}@isiskeynes.it':
                flash('L\'email non corrisponde con il nome e cognome', category='error')
            elif len(password) < 5:
                flash('La password deve essere almeno di 5 caratteri', category='error')
            elif password != password_di_conferma:
                flash('La password di conferma non e\' corretta', category='error')
            else:
                nuovo_utente = User(email=email, nome=nome, cognome=cognome,
                                    password=generate_password_hash(password, method='sha256'), punti=0, admin_user=1,account_attivo=1,
                                    classe_id=Classi.query.filter_by(classe='admin').first().id)
                db.session.add(nuovo_utente)
                admin_provvisiorio = user_da_email("s-admin.starter@isiskeynes.it")
                if admin_provvisorio and len(elenco_admin()) > 1:
                    admin_provvisiorio.delete()
                db.session.commit()
                flash('Account creato con successo!', category='success')
                login_user(nuovo_utente, remember=True)
                return redirect((url_for('pagine_sito.home')))
        return render_template("crea_admin.html", user=current_user)
