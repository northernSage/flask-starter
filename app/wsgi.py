from app import cli
from app import create_app
from app.middleware import HttpsProxyFix
from app.models import db
from app.models import Task
from app.models import User

app = create_app()
app.wsgi_app = HttpsProxyFix(app.wsgi_app)
cli.register(app)

@app.shell_context_processor
def shell_context():
    return {'db': db, 'User': User, 'Task': Task}
