from functools import wraps
from flask import redirect, url_for, session, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logado' not in session:
            flash('Você precisa estar logado para acessar esta página!')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
