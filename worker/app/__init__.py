import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from app.config import Config, TestConfig

db = SQLAlchemy()
login = LoginManager()

def create_app(test_config=None):
    """minimal app object for resource sharing
    amongst worker processes and main application
    (e.g database connection and user session info"""
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(test_config)
    db.init_app(app)
    login.init_app(app)

    return app

