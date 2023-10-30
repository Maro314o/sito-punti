from flask import Blueprint,render_template
from flask_login import login_required,current_user
from .modelli import User,Classi
pagine_sito=Blueprint('pagine_sito',__name__)

@pagine_sito.route('/')
def home():
    return render_template('home.html',user=current_user)
@pagine_sito.route('/classe')
@login_required
def classe():
    print(current_user.classe_id)
    classe=Classi.query.filter_by(id=current_user.classe_id).first()
    studenti=sorted(classe.studenti,key=lambda  studente: studente.punti)

    return render_template('classe.html',user=current_user,classe=classe.classe,studenti=classe.studenti)
@pagine_sito.route('/regole')
def regole():
    return render_template('regole.html',user=current_user)