import time
from flask import current_app

from flask_login import current_user
from tests.conftest import AuthActions

from app import db
from app.models import Task


def test_task_enqueue(client):
    actions = AuthActions(client)
    actions.register_and_login()
    Task.query.delete()
    db.session.commit()
    rv = client.get('/tasktest/1/')
    description = 'testing background jobs (1s delay)...'
    assert rv.status_code == 302
    assert rv.headers['Location'] == r'http://localhost/'
    tasks = Task.query.all()
    assert len(tasks) == 1

