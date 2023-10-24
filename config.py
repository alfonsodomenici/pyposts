import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #JWT_TOKEN_LOCATION = ["headers"]
    #JWT_SECRET_KEY = "jwt-secret"
    #JWT_HEADER_NAME = 'Authorization'
    #JWT_HEADER_TYPE = 'Bearer'

    @staticmethod
    def init_app(app):
         pass

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app_dev.db')

class TestingConfig(Config):
     TESTING=True
     SQLALCHEMY_DATABASE_URI = 'sqlite://'

class ProductionConfig(Config):
     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app_prod.db')

config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default': DevelopmentConfig
}