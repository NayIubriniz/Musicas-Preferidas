import os
from musica import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField


class FormularioMusica(FlaskForm):
    nome = StringField('Nome da música', [validators.DataRequired(),
                                          validators.Length(min=2, max=50)])

    grupo = StringField('Grupo', [validators.DataRequired(),
                                  validators.Length(min=2, max=50)])
    genero = StringField('Gênero', [validators.DataRequired(),
                                    validators.Length(min=2, max=20)])
    cadastro = SubmitField('Cadastrar Música')


class FormularioUsuario(FlaskForm):
    usuario = StringField('Usúario', [validators.DataRequired(),
                                      validators.length(min=2, max=50)])
    senha = PasswordField('Senha', [validators.DataRequired(),
                                    validators.length(min=3, max=255)])
    logar = SubmitField('Logar')


class FormularioCadastroUsuario(FlaskForm):

    nome = StringField('Nome',
                       [validators.DataRequired(),
                        validators.Length(min=2, max=50)])
    usuario = StringField('Usúario',
                          [validators.DataRequired(),
                           validators.Length(min=2, max=50)])
    senha = PasswordField('Senha',
                          [validators.DataRequired(),
                           validators.Length(min=6, max=255)])
    cadastrar = SubmitField('Cadastrar')


def recuperar_imagem(id):
    for nome_imagem in os.listdir(app.config['UPLOADS_FOLDER']):
        nome = str(nome_imagem)
        nome = nome.split('.')
        if f'album{id}_' in nome[0]:
            return nome_imagem
    return 'image-default.jpg'


def deletar_imagem(id):
    imagem = recuperar_imagem(id)
    if imagem != 'image-default.jpg':
        os.remove(os.path.join(app.config['UPLOADS_FOLDER'], imagem))
