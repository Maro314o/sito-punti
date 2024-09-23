from ..modelli import User, Classi, Info


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


def elenco_squadre():
    return set([x.squadra for x in elenco_studenti()])


def elenco_studenti_registrati():
    return [x for x in elenco_studenti() if x.account_attivo]


def get_last_season():
    return Info.query.filter_by().first().last_season
