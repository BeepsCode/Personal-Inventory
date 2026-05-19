from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'clave_super_secreta'
    
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' # Apunta al Blueprint
    
    from app.routes import main
    
    # from app.test_routes import main
    
    app.register_blueprint(main)
    
    return app