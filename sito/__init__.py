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
    LOG_FILE_PATH = os.path.join(DATA_DIRECTORY, "log.txt")
    SECRETS_DIRECTORY_PATH = os.path.join(Path.cwd(), "secrets")
    SECRET_KEY_PATH = os.path.join(SECRETS_DIRECTORY_PATH, "secret_token.txt")
    SECRET_PASSWORD_PATH = os.path.join(
        SECRETS_DIRECTORY_PATH, "secret_starter_admin_password.txt"
    )
    init_directory(SECRETS_DIRECTORY_PATH)
    init_file(SECRET_KEY_PATH)
    init_file(SECRET_PASSWORD_PATH)
    with open(SECRET_KEY_PATH, "r") as file:
        secret_key = file.read().strip()
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f'sqlite:///{os.path.join(Path.cwd(),"data",DB_NAME)}'
    )
    app.config["SOLALCHEMY_TRACK_MODIFICATIONS"] = False
    init_directory(DATA_DIRECTORY)
    init_file(ERRORS_FILE_PATH)
    init_file(LOG_FILE_PATH)
    db.init_app(app)

    from .pagine_sito import pagine_sito
    from .autenticazione import autenticazione
    import sito.database_funcs as db_funcs

    app.register_blueprint(pagine_sito, url_prefix="/")
    app.register_blueprint(autenticazione, url_prefix="/")
    from .modelli import User, Classi

    with app.app_context():
        db.create_all()
        if not db_funcs.classe_da_nome("admin"):
            db.session.add(Classi(classe="admin"))
    login_manager = LoginManager()
    login_manager.login_view = "autenticazione.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
