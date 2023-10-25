from flask import Blueprint,render_template
from flask_login import login_required,current_user
pagine_sito=Blueprint('pagine_sito',__name__)

@pagine_sito.route('/')
def home():
    return render_template('home.html',user=current_user)
@pagine_sito.route('/classe')
@login_required
def classe():
    return render_template('classe.html',user=current_user)