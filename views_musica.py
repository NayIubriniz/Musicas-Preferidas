from flask import (
    render_template, request, redirect,
    flash, url_for, send_from_directory, session
)
from utils import login_required
from models import Musica
from musica import db, app
from definicoes import (
    recuperar_imagem, deletar_imagem,
    FormularioMusica
)
import time
import os


@app.route('/musicas')
@login_required
def listarMusicas():
    from models import Usuario
    login_usuario = session['usuario_logado']
    usuario = Usuario.query.filter_by(login_usuario=login_usuario).first()

    lista = Musica.query.filter_by(usuario_id=usuario.id_usuario).order_by(
        Musica.id_musica).all()

    return render_template(
        'lista_musica.html',
        titulo='Minhas Músicas Preferidas',
        musicas=lista
    )


@app.route('/cadastrar')
@login_required
def cadastrarMusica():
    form = FormularioMusica()
    return render_template('cadastrar_musica.html', titulo='Cadastrar música',
                           form=form)


@app.route('/adicionar', methods=['POST',])
@login_required
def adicionarMusica():
    formRecebido = FormularioMusica(request.form)
    if not formRecebido.validate_on_submit():
        return redirect(url_for('cadastrarMusica'))

    nome = formRecebido.nome.data
    artista = formRecebido.grupo.data
    genero = formRecebido.genero.data
    from models import Usuario
    login_usuario = session['usuario_logado']
    usuario = Usuario.query.filter_by(login_usuario=login_usuario).first()

    if not usuario:
        flash('Usuário inválido. Faça login novamente.')
        return redirect(url_for('login'))

    musica_existente = Musica.query.filter_by(
        nome_musica=nome,
        usuario_id=usuario.id_usuario
    ).first()
    if musica_existente:
        flash('Você já cadastrou essa música!')
        return redirect(url_for('listarMusicas'))

    nova_musica = Musica(
        nome_musica=nome,
        cantor_banda=artista,
        genero_musica=genero,
        usuario_id=usuario.id_usuario
    )

    db.session.add(nova_musica)
    db.session.commit()

    arquivo = request.files['arquivo']
    if arquivo:
        pasta_arquivos = app.config['UPLOADS_FOLDER']
        nome_arquivo = arquivo.filename
        extensao = nome_arquivo.split('.')[-1]
        momento = time.time()
        nome_completo = f'album{nova_musica.id_musica}_{momento}.{extensao}'
        arquivo.save(os.path.join(pasta_arquivos, nome_completo))
        flash('Música cadastrada com sucesso!')
    return redirect(url_for('listarMusicas'))


@app.route('/editar/<int:id>')
@login_required
def editar(id):
    musica_buscada = Musica.query.filter_by(id_musica=id).first()
    form = FormularioMusica()
    form.nome.data = musica_buscada.nome_musica
    form.grupo.data = musica_buscada.cantor_banda
    form.genero.data = musica_buscada.genero_musica
    album = recuperar_imagem(id)

    return render_template('editar_musica.html',
                           titulo='Editar Música',
                           musica=form, album_musica=album, id=id)


@app.route('/atualizar', methods=['POST',])
@login_required
def atualizar():
    formRecebido = FormularioMusica(request.form)
    if formRecebido.validate_on_submit():
        musica = Musica.query.filter_by(id_musica=request
                                        .form['txtId']).first()
        musica.nome_musica = formRecebido.nome.data
        musica.cantor_banda = formRecebido.grupo.data
        musica.genero_musica = formRecebido.genero.data
        db.session.add(musica)
        db.session.commit()
        arquivo = request.files['arquivo']
        if arquivo:
            pasta_upload = app.config['UPLOADS_FOLDER']
            nome_arquivo = arquivo.filename
            nome_arquivo = nome_arquivo.split('.')
            extensao = nome_arquivo[len(nome_arquivo)-1]
            momento = time.time()
            nome_completo = f'album{musica.id_musica}_{momento}.{extensao}'
            deletar_imagem(musica.id_musica)
            arquivo.save(f'{pasta_upload}/{nome_completo}')
        flash('Música atualizada com sucesso!')
    return redirect(url_for('listarMusicas'))


@app.route('/excluir/<int:id>')
@login_required
def excluir(id):
    Musica.query.filter_by(id_musica=id).delete()
    deletar_imagem(id)
    db.session.commit()
    flash('Música excluída com sucesso!')
    return redirect(url_for('listarMusicas'))


@app.route('/uploads/<nome_imagem>')
def imagem(nome_imagem):
    return send_from_directory('uploads', nome_imagem)
