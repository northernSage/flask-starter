import os
from datetime import timedelta


class Config:
    # db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'sqlite:///../instance/app.sqlite')
    #  security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'workerkey')
    # updates
    LAST_UPDATE_DATE = '01/01/2001'
    # redis
    REDIS_URL = os.environ.get('REDIS_URL')

class TestConfig(Config):
    # db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/app.sqlite'
    SECRET_KEY = 'test'
    WTF_CSRF_ENABLED = False  # csrf protection disable when testing
