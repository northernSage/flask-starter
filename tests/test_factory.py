def test_pytest_environment(app):
    assert app.debug
    assert app.config["SECRET_KEY"] == "test"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///../instance/app.sqlite"
