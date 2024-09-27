from flask import Response, url_for, redirect

ALLOWED_EXTENSIONS = set(["xlsx"])


def allowed_files(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def errore_accesso() -> Response:
    return redirect(url_for("pagine_sito.home"))
