from app import db
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required

bp = Blueprint('homepage', __name__)

@bp.route('/')
@login_required
def index():
    return render_template( 'homepage/index.html')


@bp.route('/progress/<task_id>/')
@login_required
def get_job_progress(task_id):
    task = current_user.get_task(task_id)
    return {
        'id': task.id,
        'description': task.description,
        'progress': task.get_progress(),
        'complete': task.complete}


@bp.route('/tasktest/<delay>/')
@login_required
def testtask(delay):
    task = current_user.launch_task(
        'test_task', 
        f'testing background jobs ({delay}s delay)...', 
        delay)
    flash(f'Test job {task.id} queued')
    db.session.commit()
    return redirect(url_for('homepage.index'))
