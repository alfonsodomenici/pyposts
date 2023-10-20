from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config.from_object(Config)

"""
L'oggetto db rappresenta il database e fornisce una api con tutte le funzionalità necsesarie
"""
db = SQLAlchemy(app)

"""
Gestione dell'evoluzione dello schema relazionale
"""
migrate=Migrate(app,db)
migrate
from app import routes, models