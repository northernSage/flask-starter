def test_pytest_environment(app):
    assert app.debug  # this will always failt in production <<<
    assert app.config["MAIL_SERVER"]
    assert app.config["SECRET_KEY"] == "test"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///../instance/app.sqlite"
