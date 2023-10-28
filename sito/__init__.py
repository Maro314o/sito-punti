from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db=SQLAlchemy()
lista_classi = ['2CI']
DB_NAME='database.db'
def crea_app():

    app = Flask(__name__)
    DB_NAME = 'database.db'
    app.config['SECRET_KEY']='Speppimawwosowwi'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    app.config["SOLALCHEMY TRACK MODIFICATIONS"] = False
    db.init_app(app)

    from .pagine_sito import pagine_sito
    from .autenticazione import autenticazione

    app.register_blueprint(pagine_sito, url_prefix='/')
    app.register_blueprint(autenticazione, url_prefix='/')

    from .modelli import User,Classi
    with app.app_context():
        db.create_all()
        print('database creato')
    login_manager = LoginManager()
    login_manager.login_view = 'autenticazione.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    return app


