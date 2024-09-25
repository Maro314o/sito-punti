from sito.database_funcs.database_queries import studenti_da_classe
from ..modelli import User, Classi, Info
from .database_queries import studenti_da_classe


def elenco_utenti():
    return User.query.filter_by().all()


def elenco_studenti():

    return [utente for utente in User.query.filter_by().all() if not utente.admin_user]


def elenco_admin():
    return [utente for utente in User.query.filter_by().all() if utente.admin_user]


def elenco_tutte_le_classi():
    return Classi.query.filter_by().all()


def elenco_classi_studenti():
    return [classe for classe in elenco_tutte_le_classi() if classe.classe != "admin"]


def elenco_squadre_da_classe(classe):
    return set([x.squadra for x in studenti_da_classe(classe)])


def elenco_studenti_registrati():
    return [x for x in elenco_studenti() if x.account_attivo]


def elenco_user_da_classe_id_e_nome_squadra(classe_id, nome_squadra):

    return User.query.filter_by(classe_id=classe_id, squadra=nome_squadra).all()


def elenco_squadre_da_classe(classe):
    return {x.squadra for x in studenti_da_classe(classe)}


def get_last_season():
    return Info.query.filter_by().first().last_season
