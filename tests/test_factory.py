from app import create_app


def test_pytest_environment(app):
    assert app.debug
    assert app.config["SECRET_KEY"] == "test"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///../instance/app.sqlite"


def test_create_app(app):
    test_app = create_app() or None
    assert test_app is not None
