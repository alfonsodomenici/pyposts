from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flasgger import Swagger
"""
L'oggetto db rappresenta il database e fornisce una api con tutte le funzionalità necsesarie
"""
db = SQLAlchemy()

ma=Marshmallow()

jwt = JWTManager()

sw = Swagger()

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    ma.init_app(app)
    
    jwt.init_app(app)
    
    sw.init_app(app)
    
    #registrazione bluenprints...
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from app.api import api as api_bp
    app.register_blueprint(api_bp,url_prefix='/api')
    
    return app
