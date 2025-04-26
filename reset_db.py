from musica import app, db
from models import Usuario, Musica
import os

uploads_path = os.path.join(os.path.dirname(__file__), 'uploads')

with app.app_context():
    print('Resetando banco de dados e arquivos...')

    print('Apagando músicas...')
    Musica.query.delete()
    db.session.commit()

    print('Apagando usuários...')
    Usuario.query.delete()
    db.session.commit()

    # Aqui zera as tabelas completamente
    print('Derrubando e recriando todas as tabelas...')
    db.drop_all()
    db.create_all()

    if os.path.exists(uploads_path):
        print('Limpando arquivos da pasta uploads...')
        for filename in os.listdir(uploads_path):
            file_path = os.path.join(uploads_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    print('Reset completo! Banco de dados e arquivos limpos.')
