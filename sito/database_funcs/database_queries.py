from ..modelli import User, Classi, Cronologia


def user_da_nominativo(nominativo: str) -> User | None:
    return User.query.filter_by(nominativo=nominativo).first()


def user_da_id(id: int) -> User | None:
    return User.query.filter_by(id=id).first()


def user_da_email(email: str) -> User | None:
    return User.query.filter_by(email=email).first()


def studenti_da_classe(classe: Classi) -> list[User]:

    return classe.studenti


def classe_da_nome(classe_name: str) -> Classi | None:
    return Classi.query.filter_by(classe=classe_name).first()


def classe_da_id(classe_id: int) -> Classi | None:
    return Classi.query.filter_by(id=classe_id).first()


def cronologia_da_user(utente: User) -> list[Cronologia]:
    return utente.cronologia_studente


def evento_da_id(id: int) -> Cronologia | None:
    return Cronologia.query.filter_by(id=id).first()
