from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config


"""
L'oggetto db rappresenta il database e fornisce una api con tutte le funzionalità necsesarie
"""
db = SQLAlchemy()


def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    #registrazione bluenprints...
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from app.api import api as api_bp
    app.register_blueprint(api_bp,url_prefix='/api')
    
    return app
