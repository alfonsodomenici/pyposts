from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config.from_object(Config)

"""
L'oggetto db rappresenta il database e fornisce una api con tutte le funzionalità necsesarie
"""
db = SQLAlchemy(app)

from app import routes, models