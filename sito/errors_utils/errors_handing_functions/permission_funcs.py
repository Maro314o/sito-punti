from flask import url_for, redirect, Response

from functools import wraps
from typing import Callable, Any

from flask_login import current_user
from flask import Response, redirect, url_for


def redirect_home() -> Response:
    return redirect(url_for("pagine_sito.home"))


def admin_permission_required(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.admin_user:
            return redirect_home()
        return func(*args, **kwargs)

    return decorated_function
