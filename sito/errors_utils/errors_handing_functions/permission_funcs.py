from flask import url_for, redirect, Response

from functools import wraps
from typing import Callable, Any

from flask_login import current_user
from flask import Response, redirect, url_for


def redirect_home() -> Response:
    """
    funzione che reindirizza alla pagina home
    """
    return redirect(url_for("pagine_sito.pagina_home"))


def admin_permission_required(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    decoratore per abilitare l'accesso ad una funzione di una pagina solo agli admin.
    altrimenti riporta alla pagina home
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.admin_user:
            return redirect_home()
        return func(*args, **kwargs)

    return decorated_function
