from flask import session, redirect, url_for
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        username = session.get("login", None)
        password = session.get("password", None)
    
        if not username or not password:
            return redirect(url_for("login"))
       
        f(*args, **kwargs)
    return wrapper
