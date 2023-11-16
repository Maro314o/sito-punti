from flask import Blueprint,render_template,request
from flask_login import login_required,current_user
from .modelli import User,Classi
from werkzeug.security import generate_password_hash
pagine_sito=Blueprint('pagine_sito',__name__)

@pagine_sito.route('/')
def home():

    return render_template('home.html',user=current_user)
@pagine_sito.route('/classe',methods=["GET","POST"])
@login_required
def classe():
    
    #classe=Classi.query.filter_by(id=current_user.classe_id).first()
    classe=Classi.query.filter_by(classe='2CI').first()
    studenti=sorted(classe.studenti,key=lambda  studente: studente.punti)
    if current_user.admin_user ==1 and request.method=="POST" :
        dati=request.form
        print(dati)


    return render_template('classe.html',user=current_user,classe=classe.classe,studenti=classe.studenti)
@pagine_sito.route('/regole')
def regole():
    return render_template('regole.html',user=current_user)
@pagine_sito.route('/admin_dashboard')
@login_required
def admin_panel():
    admin_user=current_user.admin_user
    if admin_user==1:
        n_studenti=len([x for x in User.query.filter_by().all() if x.admin_user==0])
        n_classi=len(Classi.query.filter_by().all())-1
        print([x.nome for x in User.query.filter_by().all()])

        return render_template('admin_panel.html',numero_studenti=n_studenti,numero_classi=n_classi,novità=[x for x in User.query.filter_by().all()][::-1][:7])

@pagine_sito.route("/classi")
@login_required
def classi():
     admin_user=current_user.admin_user
     if admin_user==1:
            classi=[x for x in Classi.query.filter_by().all() if x.classe!='admin']
            return render_template("menù_classi.html",classi=classi)

        
