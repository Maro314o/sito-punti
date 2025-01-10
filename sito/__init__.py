from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import sito.misc_utils_funcs as mc_funcs

# DIRECTORIES
from sito.costanti import (
    DATA_DIRECTORY_PATH,
    SECRETS_DIRECTORY_PATH,
    LOGHI_DIRECTORY_PATH,
    TEMPLATE_DIRECTORY_PATH,
)

# FILE PATHS
from sito.costanti import (
    SECRET_KEY_PATH,
    FRASI_PATH,
    SECRET_PASSWORD_PATH,
    ERROR_PATH,
    LOG_PATH,
    GLOBAL_DATA_PATH,
)

# MISC
from sito.costanti import (
    INIT_BASE_KEY,
    INIT_FRASE,
    INIT_GLOBAL_DATA,
    DATABASE_LOCATION_URL,
)


db = SQLAlchemy()

app = Flask(__name__, template_folder=TEMPLATE_DIRECTORY_PATH)


def crea_app():
    mc_funcs.init_directory(DATA_DIRECTORY_PATH)
    mc_funcs.init_directory(SECRETS_DIRECTORY_PATH)
    mc_funcs.init_directory(LOGHI_DIRECTORY_PATH)
    mc_funcs.init_file(SECRET_KEY_PATH, INIT_BASE_KEY)
    mc_funcs.init_file(FRASI_PATH, INIT_FRASE)
    mc_funcs.init_file(GLOBAL_DATA_PATH, INIT_GLOBAL_DATA)

    mc_funcs.init_file(SECRET_PASSWORD_PATH)
    with open(SECRET_KEY_PATH, "r") as file:
        secret_key = file.read().strip()
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_LOCATION_URL
    app.config["SOLALCHEMY_TRACK_MODIFICATIONS"] = False
    mc_funcs.init_directory(DATA_DIRECTORY_PATH)
    mc_funcs.init_file(ERROR_PATH)
    mc_funcs.init_file(LOG_PATH)
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
