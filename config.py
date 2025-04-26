import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
usuario = os.getenv('DB_USUARIO')
senha = os.getenv('DB_SENHA')
servidor = os.getenv('DB_SERVIDOR')
database = os.getenv('DB_NOME')

SQLALCHEMY_DATABASE_URI = (
    f'mysql+mysqlconnector://{usuario}:{senha}@{servidor}/{database}'
)
UPLOADS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'uploads')
