from flask import Blueprint,render_template,request,redirect,url_for
from . import db
from flask_login import login_required,current_user
from .modelli import User,Classi
from werkzeug.security import generate_password_hash
pagine_sito=Blueprint('pagine_sito',__name__)

def user_da_email(email):
    return  User.query.filter_by(email=email).first()

def classe_da_nome(classe_name):  
    return Classi.query.filter_by(classe=classe_name).first()

def classe_da_id(classe_id):
   return Classi.query.filter_by(id=classe_id).first()

def ordina_studenti_in_modo_decrescente(classe):
    return sorted(classe.studenti,key=lambda  studente: studente.punti)[::-1]

def elenco_utenti():
    return User.query.filter_by().all()

def elenco_studenti():
    return [utente for utente in User.query.filter_by().all() if not utente.admin_user]#si potrebbe filtrare per admin_utente=0 pero' non sono sicuro del tipo che risulta (non ho voglia)
def elenco_admin():
    return [utente for utente in User.query.filter_by().all() if utente.admin_user]
def elenco_classi():#non si conta la classe degli admin 
    return [classe for classe in Classi.query.filter_by().all() if classe.classe!='admin']
def elenco_di_tutte_le_classi():
    return Classi.query.filter_by().all()

@pagine_sito.route('/')
def home():
    try:
        return render_template('home.html',user=current_user,classe_name=classe_da_id(current_user.classe.id).classe)
    except:
        return render_template('home.html',user=current_user,classe_name='non_sei_loggato_you_bozo')

@pagine_sito.route('/classe/<classe_name>',methods=["GET","POST"])
@login_required
def classe(classe_name):
    if current_user.admin_user==0:
        classe=classe_da_id(current_user.classe_id)
    else:
        classe=classe_da_nome(classe_name)
        studenti=ordina_studenti_in_modo_decrescente(classe)
    if current_user.admin_user  and request.method=="POST" :
        dati=request.form
        for email in dati:
            try:
                punti_modificati=int(dati[email])
                user_da_email(email).punti=punti_modificati
            except:
                continue
        db.session.commit() 
        studenti=ordina_studenti_in_modo_decrescente(classe)
    return render_template('classe.html',user=current_user,classe=classe.classe,studenti=studenti)

@pagine_sito.route('/regole')
def regole():
    return render_template('regole.html',user=current_user)

@pagine_sito.route('/admin_dashboard')
@login_required
def admin_panel():
    admin_user=current_user.admin_user
    if admin_user==1:
        numero_degli_studenti=len(elenco_studenti())
        numero_delle_classi=len(elenco_classi()) 
        return render_template('admin_panel.html',numero_studenti=numero_degli_studenti,numero_classi=numero_delle_classi,novità=elenco_utenti()[::-1][:7])

@pagine_sito.route("/classi",methods=["GET","POST"])
@login_required
def classi():
 
     if current_user.admin_user:
            classi=elenco_classi()

            if request.method=='POST': 
                dati=request.form
                classe_name=dati.get('classe')
                classe=classe_da_nome(classe_name)
                return redirect(url_for('pagine_sito.classe',classe_name=classe.classe))
            return render_template('menù_classi.html')

     

        
