from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flasgger import Swagger

template = {
  "swagger": "2.0",
  "info": {
    "title": "Py POST APP",
    "description": "API for my data",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "me@me.com",
      "url": "www.me.com",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
  "host": "127.0.0.1:5000",  # overrides localhost:500
  "basePath": "/api/users",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}



db = SQLAlchemy()

ma = Marshmallow()

jwt = JWTManager()

sw = Swagger(template=template)

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    #config[config_name].init_app(app)
    
    db.init_app(app)

    ma.init_app(app)

    jwt.init_app(app)

    sw.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
