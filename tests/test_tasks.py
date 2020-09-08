from time import sleep

from app import db
from app.models import Task
from tests.conftest import AuthActions


def _clean_set_up(client):
    actions = AuthActions(client)
    actions.register_and_login()
    Task.query.delete()
    db.session.commit()


def test_task_enqueue(client):
    _clean_set_up(client)
    rv = client.get("/tasktest/1/")
    assert rv.status_code == 302
    assert rv.headers["Location"] == r"http://localhost/"
    tasks = Task.query.all()
    assert len(tasks) == 1


def test_task_multiple_enqueues(client):
    _clean_set_up(client)
    for _ in range(3):
        client.get("/tasktest/0/")
    sleep(1)
    tasks = Task.query.all()
    assert len(tasks) == 3


def test_task_should_complete(client):
    _clean_set_up(client)
    for _ in range(3):
        client.get("/tasktest/0/")
    sleep(5)
    tasks = Task.query.all()
    for task in tasks:
        assert task.complete


def test_per_user_task_separation(client):
    _clean_set_up(client)
    client.get("/tasktest/10/")
    task = Task.query.filter_by(user_id=1).first()
    assert task
    # logout default test user
    AuthActions(client).logout()
    actions = AuthActions(
        client, username="appuser2", password="appuser2", email="appuser2@gmail.com"
    )
    actions.register_and_login()
    task = Task.query.filter_by(user_id=2).first()
    assert not task


#    client.get("/tasktest/10/")

# task = Task.query.filter_by(user_id=2).first()
# assert task
