from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

csrf = CSRFProtect(app)

from views_musica import *  # noqa: F401, E402, F403
from views_usuario import *  # noqa: F401, E402, F403

if __name__ == '__main__':
    app.run(debug=True)
