from ..modelli import User, Classi, Cronologia


def cronologia_da_user(utente):
    return utente.cronologia_studente


def user_da_nominativo(nominativo):
    return User.query.filter_by(nominativo=nominativo).first()


def user_da_id(id):
    return User.query.filter_by(id=id).first()


def user_da_email(email):
    return User.query.filter_by(email=email).first()


def classe_da_nome(classe_name):
    return Classi.query.filter_by(classe=classe_name).first()


def classe_da_id(classe_id):
    return Classi.query.filter_by(id=classe_id).first()


def studenti_da_classe(classe):

    return classe.studenti


def evento_da_id(id):
    return Cronologia.query.filter_by(id=id).first()
