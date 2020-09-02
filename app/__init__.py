
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue

from flask_mail import Mail

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()


def create_app(test_config=None):
    """App factory"""
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(test_config)
    # error handing 
    if not app.debug:
        #  mail logger
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Error Log',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        # rotating file logger
        log_path = Path('app/logs/error.log')
        log_path.parent.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10240,
            backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Starting up...')

    #  creating instance folder 
    Path(app.instance_path).mkdir(exist_ok=True)

    # initializing extensions 
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    login.login_view = 'auth.login'

    # setting up redis 
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = Queue('task-queue', connection=app.redis)

    #  registering blueprints
    from .blueprints import auth
    app.register_blueprint(auth.bp)
    from .blueprints import homepage
    app.register_blueprint(homepage.bp)
    from .blueprints import error
    app.register_blueprint(error.bp)
    from .blueprints import email
    app.register_blueprint(email.bp)

    return app
