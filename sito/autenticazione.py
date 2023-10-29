from flask import Blueprint,render_template,request,flash,redirect,url_for
from .modelli import User,Classi
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import lista_classi
autenticazione=Blueprint('autenticazione',__name__)

def campi_vuoti(dati):
    for campo in dati.values():
        if campo == '':
            return True
    return False
def crea_classe(lista_delle_classi):
    for nome_della_classe in lista_delle_classi:
        if not Classi.query.filter_by(classe=nome_della_classe).first():

            db.session.add(Classi(classe=nome_della_classe))
            db.session.commit()





@autenticazione.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email does not exist.', category='error')
        elif not check_password_hash(user.password, password):
            flash('Incorrect password, try again.', category='error')
        else:

            login_user(user, remember=True)
            return redirect(url_for('pagine_sito.classe'))
    return render_template("login.html", user=current_user)



@autenticazione.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('autenticazione.login'))


@autenticazione.route("/sign_up",methods=['GET','POST'])
def sign_up():
    crea_classe(lista_classi)
    if request.method=='POST':

        dati=request.form

        email = dati.get('email').lower()
        nome = dati.get('nome').capitalize()
        cognome = dati.get('cognome').capitalize()
        password = dati.get('password')
        password_di_conferma = dati.get('password_di_conferma')
        nome_classe=dati.get('classe')

        classe=Classi.query.filter_by(classe=nome_classe).first()


        user = User.query.filter_by(email=email).first()


        if campi_vuoti(dati) is True:
            flash('Devi compilare tutti i campi', category='error')
        elif user:
            flash('Esiste gia\' un account con questa email',category='error')
        elif '@isiskeynes.it' not in email:
            flash('Il dominio dell\' email é sbagliato', category='error')
        elif 's-' not in email:
            flash('hai dimenticato di mettere \'s-\' nell\' email', category='error')
        elif email != f's-{cognome.lower()}.{nome.lower()}@isiskeynes.it':
            flash('L\'email non corrisponde con il nome e cognome', category='error')
        elif classe is None:
            flash('Seleziona una classe', category='error')
        elif len(password) < 5:
            flash('La password deve essere almeno di 5 caratteri', category='error')
        elif password != password_di_conferma:
            flash('La password di conferma non e\' corretta', category='error')
        else:
            nuovo_utente= User(email=email, nome=nome,cognome=cognome,password=generate_password_hash(password,method='sha256'),punti=0,classe_id=classe.id)
            db.session.add(nuovo_utente)
            db.session.commit()
            flash('Account creato con successo!', category='success')
            return redirect((url_for('pagine_sito.classe')))







    return render_template("sign_up.html",user=current_user,lista_classi=lista_classi)