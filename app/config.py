import os


class Config:
    # db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///../instance/app.sqlite"
    )
    #  security
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    # updates
    LAST_UPDATE_DATE = "01/01/2001"
    # redis
    REDIS_URL = os.environ.get("REDIS_URL", r"redis://redis_queue:6379/0")
    # email
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    adm_emails = os.environ.get("ADMINS", "app@email.com.br").split(",")
    ADMINS = [*adm_emails]


class TestConfig(Config):
    # db
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/app.sqlite"
    SECRET_KEY = "test"
    MAIL_SERVER = ""
    WTF_CSRF_ENABLED = False  # csrf protection disabled for testing
    DEBUG = True
    REDIS_URL = r"redis://redis_queue:6379/0"
