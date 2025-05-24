from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    # --- CAMPOS ALTERADOS E NOVOS ---
    nome_completo = db.Column(db.String(150), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) # Trocamos username por email
    password_hash = db.Column(db.String(512), nullable=False) # Aumentado o tamanho
    # --- FIM DAS ALTERAÇÕES ---
    admin = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

class Veiculo(db.Model):
    __tablename__ = 'veiculos'
    
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(64), nullable=False)
    marca = db.Column(db.String(64), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    placa = db.Column(db.String(10), unique=True, nullable=False)
    cor = db.Column(db.String(32), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)