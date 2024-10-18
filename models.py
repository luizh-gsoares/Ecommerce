import re
from datetime import datetime
from abc import abstractmethod, ABC
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AnakinSkywalker64209'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/ecomerce.sqllite3'


# Singleton do Banco de Dados
class Database:
    _instance = None

    def __new__(cls, app):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.db = SQLAlchemy(app)
        return cls._instance


# Criação da instância do banco de dados usando Singleton
db = Database(app).db


# region Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'

class Product(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'<Produto {self.name}>'
# endregion

# Adiciona um usuário administrador
def add_admin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password='admin', is_admin=True)
        db.session.add(admin)
        db.session.commit()

# region Banco de Dados
with app.app_context():
    db.create_all()
    db.session.commit()
    add_admin()
    
# endregion
