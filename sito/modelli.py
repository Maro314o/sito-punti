from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email =db.Column(db.String(150),unique=True)
    nome=db.Column(db.String(150))
    cognome =db.Column(db.String(150))
    password =db.Column(db.String(150))
    punti=db.Column(db.Integer)
    admin_user=db.Column(db.Integer)
    classe_id=db.Column(db.Integer,db.ForeignKey('classi.id'))

class Classi(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    classe=db.Column(db.String(150),unique=True)
    studenti=db.relationship('User')

