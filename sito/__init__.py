from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path

import sito.misc_utils_funcs as mc_funcs

db = SQLAlchemy()

template_dir = os.path.join(Path.cwd(), "sito", "static", "html")
app = Flask(__name__, template_folder=template_dir)


def crea_app():
    DB_NAME = "database.db"
    DATA_DIRECTORY = os.path.join(Path.cwd(), "data")
    ERRORS_FILE_PATH = os.path.join(DATA_DIRECTORY, "errore.txt")
    LOG_FILE_PATH = os.path.join(DATA_DIRECTORY, "log.txt")
    LOGHI_FILE_PATH = os.path.join(Path.cwd(), "sito", "static", "images", "loghi")
    SECRETS_DIRECTORY_PATH = os.path.join(Path.cwd(), "secrets")
    SECRET_KEY_PATH = os.path.join(SECRETS_DIRECTORY_PATH, "secret_token.txt")
    GLOBAL_DATA_PATH = os.path.join(DATA_DIRECTORY, "global_data.json")
    FRASI_PATH = os.path.join(DATA_DIRECTORY, "frasi.json")
    SECRET_PASSWORD_PATH = os.path.join(
        SECRETS_DIRECTORY_PATH, "secret_starter_admin_password.txt"
    )
    standard_base_key = "standardbasekey"
    mc_funcs.init_directory(DATA_DIRECTORY)
    mc_funcs.init_directory(SECRETS_DIRECTORY_PATH)
    mc_funcs.init_directory(LOGHI_FILE_PATH)
    mc_funcs.init_file(SECRET_KEY_PATH, standard_base_key)
    mc_funcs.init_file(
        FRASI_PATH,
        '[{"autore":"anonimo","frase":"Ci sono 10 tipi di persone al mondo: quelle che capiscono il codice binario e quelle che non lo capiscono.","data":"1970-1-1"}]',
    )
    mc_funcs.init_file(
        GLOBAL_DATA_PATH, '{"stagione":0,"ultimo_upload":0,"ultima_modifica":0}'
    )

    mc_funcs.init_file(SECRET_PASSWORD_PATH)
    with open(SECRET_KEY_PATH, "r") as file:
        secret_key = file.read().strip()
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f'sqlite:///{os.path.join(Path.cwd(),"data",DB_NAME)}'
    )
    app.config["SOLALCHEMY_TRACK_MODIFICATIONS"] = False
    mc_funcs.init_directory(DATA_DIRECTORY)
    mc_funcs.init_file(ERRORS_FILE_PATH)
    mc_funcs.init_file(LOG_FILE_PATH)
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

            db_funcs.crea_squadra(nome_squadra="admin", classe_name="admin")
            db.session.commit()
    login_manager = LoginManager()
    login_manager.login_view = "autenticazione.pagina_login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
