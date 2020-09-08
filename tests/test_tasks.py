from time import sleep

from app import db
from app.models import Task
from tests.conftest import AuthActions


def test_task_enqueue(client):
    actions = AuthActions(client)
    actions.register_and_login()
    Task.query.delete()
    db.session.commit()
    rv = client.get("/tasktest/1/")
    assert rv.status_code == 302
    assert rv.headers["Location"] == r"http://localhost/"
    tasks = Task.query.all()
    assert len(tasks) == 1


def test_task_should_complete(client):
    actions = AuthActions(client)
    actions.register_and_login()
    Task.query.delete()
    db.session.commit()
    client.get("/tasktest/0/")
    sleep(5)
    task = Task.query.first()
    assert task.complete
