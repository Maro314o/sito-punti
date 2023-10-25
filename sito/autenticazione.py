from flask import Blueprint,render_template,request,flash,redirect,url_for
from .modelli import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
autenticazione=Blueprint('autenticazione',__name__)
def campi_vuoti(dati):
    for campo in dati.values():

        if campo == '':
            return True
    return False



@autenticazione.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                print('cancer')
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('pagine_sito.classe'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
        print('balls')
    return render_template("login.html", user=current_user)



@autenticazione.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('autenticazione.login'))


@autenticazione.route("/sign_up",methods=['GET','POST'])
def sign_up():
    if request.method=='POST':

        dati=request.form

        email = dati.get('email').lower()
        nome = dati.get('nome')
        cognome = dati.get('cognome')
        password = dati.get('password')
        password_di_conferma = dati.get('password_di_conferma')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Esiste gia\' un account con questa email',category='error')
        if campi_vuoti(dati) is True:

            flash('Devi compilare tutti i campi', category='error')
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
            nuovo_utente= User(email=email, nome=nome,cognome=cognome,password=generate_password_hash(password,method='sha256'),classe='2CI',punti=0)
            db.session.add(nuovo_utente)
            db.session.commit()
            flash('Account creato con successo!', category='success')
            return redirect((url_for('pagine_sito.home')))







    return render_template("sign_up.html",user=current_user)