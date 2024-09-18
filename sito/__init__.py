from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path
from .misc_utils_funcs import init_directory, init_file

db = SQLAlchemy()

template_dir = os.path.join(Path.cwd(), "sito", "static", "html")
app = Flask(__name__, template_folder=template_dir)


def crea_app():
    DB_NAME = "database.db"
    DATA_DIRECTORY = "data"
    ERRORS_FILE_PATH = os.path.join(DATA_DIRECTORY, "errore.txt")
    app.config["SECRET_KEY"] = "Speppimawwosowwi"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f'sqlite:///{os.path.join(Path.cwd(),"data",DB_NAME)}'
    )
    app.config["SOLALCHEMY_TRACK_MODIFICATIONS"] = False
    init_directory(DATA_DIRECTORY)
    init_file(ERRORS_FILE_PATH)
    db.init_app(app)

    from .pagine_sito import pagine_sito
    from .autenticazione import autenticazione

    app.register_blueprint(pagine_sito, url_prefix="/")
    app.register_blueprint(autenticazione, url_prefix="/")
    from .modelli import User

    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    login_manager.login_view = "autenticazione.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
