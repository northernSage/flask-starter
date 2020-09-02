import pytest
from app import create_app
from app import db
from app.config import TestConfig
from app.models import User


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions:
    """common authentication actions for testing"""

    def __init__(
        self, client, username="test", password="test", email="test@gmail.com"
    ):
        self._email = email
        self._client = client
        self._username = username
        self._password = password
        self._is_authenticated = False
        self._is_registered = False

    def get_logged_user(self):
        if self._is_authenticated:
            return User.query.filter_by(username=self._username).first()
        return None

    def register_and_login(self):
        if not User.query.filter_by(username="test").first():
            self.register()
        self.login()

    def login(self):
        rv = self._client.post(
            "/auth/login/",
            data={"username": self._username, "password": self._password},
        )
        if rv.status_code == 302:
            self._is_authenticated = True

    def register(self):
        rv = self._client.post(
            "/auth/register/",
            data={
                "username": self._username,
                "email": self._email,
                "password": self._password,
                "password2": self._password,
            },
        )
        user = User.query.filter_by(username=self._username).first()
        if rv.status_code == 302 and user is not None:
            self._is_registered = True

    def logout(self):
        self._client.get("/auth/logout/")
        self._is_authenticated = False
