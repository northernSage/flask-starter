from tests.conftest import AuthActions

from app import db
from app.models import User

from flask_login import current_user


def test_login_get_should_return_200(client):
    rv = client.get('auth/login/')
    assert rv.status_code == 200


def test_login_get_should_show_form(client):
    rv = client.get('auth/login/')
    assert b'form action="" method="POST"' in rv.data


def test_login_post_no_data(client):
    rv = client.post('auth/login/', data={})
    assert rv.status_code == 200
    assert b'form action="" method="POST"' in rv.data


def test_login_post_wrong_data(client):
    rv = client.post('auth/login/', data={'wrong-key': 'wrong-value'})
    assert rv.status_code == 200
    assert b'form action="" method="POST"' in rv.data


def test_register_post_creates_user(client):
    user_data = {
        'username': 'newuser',
        'email': 'newuser@gmail.com',
        'password': 'newuserpassword',
        'password2': 'newuserpassword',
    }
    rv = client.post('/auth/register/', data={**user_data})
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/auth/login/'
    user = User.query.filter_by(username=user_data['username']).first()
    assert user is not None
    db.session.delete(User.query.filter_by(username='newuser').first())
    db.session.commit()


def test_known_user_should_authenticate(client):
    actions = AuthActions(client)
    actions.register_and_login()
    # try getting login-required page
    rv = client.get('/')
    assert rv.status_code == 200


def test_auth_view_guard(client):
    rv = client.get('/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == r'http://localhost/auth/login/?next=%2F'
    rv = client.get('/tasktest/3/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == r'http://localhost/auth/login/?next=%2Ftasktest%2F3%2F'


def test_register_get_should_return_200(client):
    rv = client.get('/auth/register/')
    assert rv.status_code == 200


def test_register_get_should_show_form(client):
    rv = client.get('/auth/register/')
    assert b'form action="" method="post"' in rv.data


def test_register_post_empty_data(client):
    rv = client.post('/auth/register/', data={})
    assert rv.status_code == 200
    assert b'form action="" method="post"' in rv.data


def test_register_post_wrong_data(client):
    rv = client.post('/auth/register/', data={'wrong': 'data'})
    assert rv.status_code == 200
    assert b'form action="" method="post"' in rv.data


def test_register_when_authenticated(client):
    actions = AuthActions(client)
    actions.register_and_login()
    rv = client.get('/auth/register/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/'


def test_login_when_authenticated(client):
    actions = AuthActions(client)
    actions.register_and_login()
    rv = client.get('/auth/login/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/'


def test_logout(client):
    actions = AuthActions(client)
    actions.register_and_login()
    rv = client.get('/auth/logout/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'http://localhost/auth/login/'
    rv = client.get('/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == r'http://localhost/auth/login/?next=%2F'


def test_register_existing_users(client):
    actions = AuthActions(client)
    actions.register()
    user_data = { # same as test user
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'password2': 'test'}
    for i in range(5):
        rv = client.post('/auth/register/', data={**user_data})
        assert rv.status_code == 200
    users = User.query.filter_by(username='test').all()
    assert len(users) == 1


def test_logout_when_not_logged_in(client):
    rv = client.get('/auth/logout/')
    assert rv.status_code == 302
    assert rv.headers['Location'] == r'http://localhost/auth/login/?next=%2Fauth%2Flogout%2F'

