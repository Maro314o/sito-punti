from flask import Flask, render_template
import json
def crea_app():

    app = Flask(__name__)
    app.config['SECRET_KEY']='Speppimawwosowwi'
    from .pagine_sito import pagine_sito
    from .autenticazione import autenticazione

    app.register_blueprint(pagine_sito, url_prefix='/')
    app.register_blueprint(autenticazione, url_prefix='/')
    return app


