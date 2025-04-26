from musica import db


class Musica(db.Model):
    id_musica = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_musica = db.Column(db.String(50), nullable=False)
    cantor_banda = db.Column(db.String(50), nullable=False)
    genero_musica = db.Column(db.String(20), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'),
                           nullable=False)

    usuario = db.relationship('Usuario', back_populates='musicas')

    def __repr__(self):
        return f'<Musica {self.nome_musica}>'


class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(50), nullable=False)
    login_usuario = db.Column(db.String(50), nullable=False)
    senha_usuario = db.Column(db.String(255), nullable=False)
    musicas = db.relationship('Musica', back_populates='usuario')

    def __repr__(self):
        return f'<Usuario {self.nome_usuario}>'
