from .. import db


def elimina_evento_cronologia(evento):
    db.session.delete(evento)


def cronologia_utente(utente, stagione):
    return [x for x in utente.cronologia_studente if x.stagione == stagione]
