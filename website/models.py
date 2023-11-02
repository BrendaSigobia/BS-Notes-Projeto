from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    primeiro_nome = db.Column(db.String(150))
    notas = db.relationship('Nota')


class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(50000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
