from flask import Blueprint,render_template

pagine_sito=Blueprint('pagine_sito',__name__)

@pagine_sito.route('/')
def home():
    return render_template('home.html')