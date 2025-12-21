from flask import (
    Blueprint,
    Response,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
)
from sito.costanti import  FRASI_PATH, LOGHI_DIRECTORY_PATH 
from sito.database_funcs.classify_by_points import ottieni_punti_parziali
import sito.errors_utils as e_utils
from sito.modelli.classe import Classe
from sito.modelli.utente import Utente
from . import  app

with app.app_context():
    import sito.database_funcs as db_funcs
import sito.misc_utils_funcs as mc_utils



from flask_login import login_required, current_user
from .modelli import Info
from os import  listdir

from math import ceil, sqrt

pagine_sito = Blueprint("pagine_sito", __name__)


@pagine_sito.route("/")
def pagina_home() -> str:
    classe_name = None
    if current_user.is_authenticated:
        classe_name = Classe.da_id(current_user.classe_id).nome_classe
    loghi = [logo for logo in listdir(LOGHI_DIRECTORY_PATH)]
    lenght_square_of_loghi = ceil(sqrt(len(loghi)))
    frase = mc_utils.get_random_json_item(FRASI_PATH)
    last_season = Info.ottieni_ultima_stagione()
    return render_template(
        "home.html",
        user=current_user,
        classe_name=classe_name,
        lista_loghi=loghi,
        lenght_square_of_loghi=lenght_square_of_loghi,
        frase=frase,
        last_season=last_season,
    )


@pagine_sito.route("/classe/<classe_name>/<int:stagione>", methods=["GET", "POST"])
@login_required
def pagina_classe(
    classe_name: str,
    stagione: int,
) -> str:
    if current_user.admin_user:
        classe = Classe.da_nome(classe_name)
    else:
        classe = Classe.da_id(current_user.classe_id)
    studenti = db_funcs.classifica_studenti_di_una_classe(stagione, classe)
    n_stagioni = Info.ottieni_ultima_stagione()
    loghi = {logo.rsplit(".", 1)[0]: logo for logo in listdir(LOGHI_DIRECTORY_PATH)}
    return render_template(
        "classe.html",
        user=current_user,
        classe=classe,
        studenti=studenti,
        n_stagioni=n_stagioni,
        stagione_corrente=stagione,
        elenco_date=lambda eventi: [evento.data for evento in eventi],
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
        zip=zip,
        url_name=mc_utils.insert_underscore_name,
        classifica_squadre=db_funcs.classifica_squadre,
        loghi=loghi,
    )


@pagine_sito.route(
    "/classe/<classe_name>/<int:stagione>/<nominativo_con_underscore>",
    methods=["GET"],
)
@login_required
def pagina_info_studente(
    classe_name: str,
    stagione: int,
    nominativo_con_underscore: str,
) -> str | Response:
    if (
        mc_utils.insert_underscore_name(current_user.nominativo)
        != nominativo_con_underscore
        and not current_user.admin_user
    ):
        return e_utils.redirect_home()
    nominativo = mc_utils.remove_underscore_name(nominativo_con_underscore)
    loghi = {logo.rsplit(".", 1)[0]: logo for logo in listdir(LOGHI_DIRECTORY_PATH)}
    studente = Utente.da_nominativo(nominativo)
    return render_template(
        "info_studente.html",
        user=current_user,
        stagione_corrente=stagione,
        studente=studente,
        elenco_date=lambda eventi: [evento.data for evento in eventi],
        calcola_valore_rgb=mc_utils.calcola_valore_rgb,
        lista_parziale=ottieni_punti_parziali(studente.elenco_cronologia_stagione(stagione)),
        elenco_attivita=lambda eventi: [evento.attivita for evento in eventi],
        zip=zip,
        classe=classe_name,
        loghi=loghi,
    )


@pagine_sito.route("/regole")
def pagina_regole() -> str:
    classe_name = None
    if current_user.is_authenticated:
        classe_name = Classe.da_id(current_user.classe_id).nome_classe
    return render_template("regole.html", user=current_user, classe_name=classe_name)


@pagine_sito.route("/coming_soon")
def pagina_comingsoon() -> str:
    classe_name = None
    if current_user.is_authenticated:
        classe_name = Classe.da_id(current_user.classe_id).nome_classe
    return render_template(
        "coming_soon.html", user=current_user, classe_name=classe_name
    )


