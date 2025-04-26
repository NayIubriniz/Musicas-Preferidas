from flask import render_template, request, redirect, session, flash, url_for
from musica import app, db
from definicoes import FormularioUsuario, FormularioCadastroUsuario
from flask_bcrypt import generate_password_hash, check_password_hash


@app.before_request
def require_login():
    rotas_livres = [
        'login', 'autenticar', 'cadastrar_usuario',
        'adicionar_usuario', 'static', 'index'
    ]
    endpoint = request.endpoint
    if endpoint is None:
        return
    if 'usuario_logado' not in session and endpoint not in rotas_livres:

        if request.method == 'GET':
            flash('Você precisa estar logado para acessar essa página.')
        return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/logar')
def login():
    form = FormularioUsuario()
    return render_template('login.html', form=form)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    from models import Usuario
    form = FormularioUsuario(request.form)
    usuario = Usuario.query.filter_by(login_usuario=form.usuario.data).first()
    if usuario is None:
        flash('Usuário não encontrado!')
        return redirect(url_for('login'))
    senha_valida = check_password_hash(usuario.senha_usuario, form.senha.data)
    if senha_valida:
        session['usuario_logado'] = usuario.login_usuario

        flash(f'Bem-vindo(a) {usuario.login_usuario}!')
        return redirect(url_for('listarMusicas'))
    else:
        flash('Senha incorreta!')
        return redirect(url_for('login'))


@app.route('/cadastrarUsuario')
def cadastrar_usuario():
    if 'usuario_logado' in session:
        flash('Você já está logado!')
        return redirect(url_for('listarMusicas'))
    form = FormularioCadastroUsuario()
    return render_template('cadastro_usuario.html',
                           titulo='Cadastro de Usuário', form=form,
                           ocultar_nav=True)


@app.route('/addUsuario', methods=['POST',])
def adicionar_usuario():
    formRecebido = FormularioCadastroUsuario(request.form)
    if not formRecebido.validate_on_submit():
        return redirect(url_for('cadastro_usuario'))
    nome = formRecebido.nome.data
    usuario = formRecebido.usuario.data
    senha = generate_password_hash(formRecebido.senha.data).decode('utf-8')
    from models import Usuario
    usuario_existe = Usuario.query.filter_by(login_usuario=usuario).first()
    if usuario_existe:
        flash('Usuário já cadastrado!')
        return redirect(url_for('cadastrar_usuario'))
    novo_usuario = Usuario(nome_usuario=nome, login_usuario=usuario,
                           senha_usuario=senha)
    db.session.add(novo_usuario)
    db.session.commit()
    session
    flash('Usuário cadastrado com sucesso!')
    return redirect(url_for('listarMusicas'))


@app.route('/sair')
def sair():
    session.pop('usuario_logado', None)
    flash('Usuário deslogado com sucesso!')
    return redirect('login')
