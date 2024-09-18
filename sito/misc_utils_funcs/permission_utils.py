from flask import url_for, redirect

ALLOWED_EXTENSIONS = set(["xlsx"])


def allowed_files(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def errore_accesso():
    return redirect(url_for("pagine_sito.home"))
