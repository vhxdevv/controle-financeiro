from main import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, Primary_Key=True)
    email = db.Column
    senha = db.Column
    transaçoes = db.relationship

class Transaçao(db.Model):
    id = db.Column
    tipo = db.Column
    valor = db.Column
    descriçao = db.Column
    categoria = db.Column
    data = db.Column
    user_id = db.Column