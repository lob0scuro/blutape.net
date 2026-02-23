from flask import Flask
from config import Config
from .extensions import db, migrate, bcrypt, cors, login_manager, session, mail
from .models import User
from .logging_config import LoggingConfig
from itsdangerous import URLSafeTimedSerializer

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    LoggingConfig.setup(app)
    
    #EXTENTIONS
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)
    login_manager.init_app(app) 
    session.init_app(app) 
    mail.init_app(app)
    
    from . import extensions
    extensions.serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    
    
    #blueprints
    from .api import api_bp
    app.register_blueprint(api_bp)
    
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    return app