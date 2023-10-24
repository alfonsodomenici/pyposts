from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()


def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    #config[config_name].init_app(app)
    
    db.init_app(app)

    jwt = JWTManager(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
