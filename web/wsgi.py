from app import cli, create_app
from app.models import Task, User, db
from app.middleware import HttpsProxyFix

app = create_app()
app.wsgi_app = HttpsProxyFix(app.wsgi_app)
cli.register(app)

@app.shell_context_processor
def shell_context():
    return {'db': db, 'User': User, 'Task': Task}

