from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

# ALTERAÇÃO: Redireciona para a rota de cadastro de usuário
# O nome da rota será 'main.register_user' que criaremos no passo 4
login_manager.login_view = 'main.register_user'
login_manager.login_message = "Você precisa se cadastrar ou fazer login para acessar esta página."
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    db.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    # Importante: O user_loader deve estar associado ao login_manager
    # dentro da factory para evitar problemas de contexto da aplicação.
    from app.models import Usuario
    
    @login_manager.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))
        
    return app