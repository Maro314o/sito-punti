from flask import Blueprint,render_template,request,flash,redirect,url_for
from .modelli import User,Classi
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
autenticazione=Blueprint('autenticazione',__name__)

def campi_vuoti(dati):
    for campo in dati.values():
        if campo == '':
            return True
    return False
def crea_classe():
           lista_classi=Classi.query.filter_by().all()
           lista_classi=[x.classe for x in lista_classi]
           lista_classi.remove('admin')
           return lista_classi


@autenticazione.route('/login',methods=['GET','POST'])
def login():
    if len(Classi.query.filter_by().all())==0:
        db.session.add(Classi(classe='admin'))
        db.session.commit
        nuovo_utente= User(email="s-admin.starter@isiskeynes.it", nome='admin',cognome="starter",password=generate_password_hash("highsecureadminpassword",method='sha256'),punti=0,admin_user=1,classe_id=Classi.query.filter_by(classe='admin').first().id)
        db.session.add(nuovo_utente)
        db.session.commit()

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
            return redirect(url_for('pagine_sito.home'))
    return render_template("login.html", user=current_user)



@autenticazione.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('pagine_sito.home'))


@autenticazione.route("/sign_up",methods=['GET','POST'])
def sign_up():
    lista_classi=crea_classe()
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
            nuovo_utente= User(email=email, nome=nome,cognome=cognome,password=generate_password_hash(password,method='sha256'),punti=0,admin_user=0,classe_id=classe.id)
            db.session.add(nuovo_utente)
            db.session.commit()

            flash('Account creato con successo!', category='success')
            login_user(nuovo_utente, remember=True)
            return redirect((url_for('pagine_sito.home')))







    return render_template("sign_up.html",user=current_user,lista_classi=lista_classi)
@autenticazione.route("/crea_admin",methods=["GET","POST"])
@login_required
def crea_admin():
    admin_user=current_user.admin_user
    if admin_user==1:
        if request.method=='POST':

            dati=request.form

            email = dati.get('email').lower()
            nome = dati.get('nome').capitalize()
            cognome = dati.get('cognome').capitalize()
            password = dati.get('password')
            password_di_conferma = dati.get('password_di_conferma')



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
            elif len(password) < 5:
                flash('La password deve essere almeno di 5 caratteri', category='error')
            elif password != password_di_conferma:
                flash('La password di conferma non e\' corretta', category='error')
            else:
                nuovo_utente= User(email=email, nome=nome,cognome=cognome,password=generate_password_hash(password,method='sha256'),punti=0,admin_user=1,classe_id=Classi.query.filter_by(classe='admin').first().id)
                db.session.add(nuovo_utente)
                db.session.commit()
                if User.query.filter_by(email="s-admin.starter@isiskeynes.it") and len(User.query.filter_by(admin_user=1).all()) >1:
                    User.query.filter_by(email="s-admin.starter@isiskeynes.it").delete()
                    db.session.commit()
                flash('Account creato con successo!', category='success')
                login_user(nuovo_utente, remember=True)
                return redirect((url_for('pagine_sito.home')))
        return render_template("crea_admin.html",user=current_user)

