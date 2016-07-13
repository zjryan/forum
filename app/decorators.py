from flask import abort
from functools import wraps
from .models import current_user


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            abort(405)
        return f(*args, **kwargs)
    return wrapped
