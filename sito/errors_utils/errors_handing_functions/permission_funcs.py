from flask import url_for, redirect, Response
from functools import wraps
from typing import Callable, Any
from flask_login import current_user


def redirect_home() -> Response:
    """
    Reindirizza l'utente alla pagina home.

    Returns:
        Response: Oggetto di risposta Flask che effettua il redirect alla home.
    """
    return redirect(url_for("pagine_sito.pagina_home"))


def admin_permission_required(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decoratore per limitare l'accesso di una funzione solo agli utenti admin.

    Se l'utente corrente non è admin, viene reindirizzato alla pagina home.

    Args:
        func (Callable[..., Any]): Funzione della route da proteggere.

    Returns:
        Callable[..., Any]: Funzione decorata che controlla i permessi admin.
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.admin_user:
            return redirect_home()
        return func(*args, **kwargs)

    return decorated_function
