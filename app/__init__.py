from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    
    # Create a Flask app instance
    app = Flask(__name__)
    # Loading config from config class
    app.config.from_object(config_class)
    
    # Initialize the extensions with the app instance
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Setting the login view for login
    login_manager.login_view = 'auth.login'
    
    # Registering the authentication blueprint
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp,url_prefix='/auth')
    
    # Registering the main blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app


@login_manager.user_loader
def load_user(user_id):
    # Function to load a user given their ID
    from app.models import User
    return User.query.get(int(user_id))