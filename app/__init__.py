from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # Adicionando o LoginManager
from config import Config

# Cria o objeto db aqui
db = SQLAlchemy()
login_manager = LoginManager()  # Instanciando o LoginManager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

     # Configura o LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Definindo a rota de login

    # Inicializa o db com o app
    db.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app
