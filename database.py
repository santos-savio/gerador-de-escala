from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def init_db(app):
    """Inicializa o banco de dados com a aplicação Flask"""
    # Configuração do SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'escala.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Garante que a pasta instance existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    
    # Cria as tabelas
    with app.app_context():
        db.create_all()
