from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from app.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm
from app import db

bp = Blueprint('homepage', __name__)

@bp.route('/')
def index():
    forms = {}
    if not current_user.is_authenticated:
        forms['login_form'] = LoginForm()
        forms['register_form'] = RegistrationForm()
        forms['reset_request_form'] = ResetPasswordRequestForm()
    return render_template(
        'homepage/index.html', 
        login_form=forms.get('login_form'), 
        register_form=forms.get('register_form'),
        reset_request_form=forms.get('reset_request_form'))


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
        'test_task', f'testing background jobs ({delay}s delay)...', delay)
    flash(f'Test job {task.id} queued')
    db.session.commit()
    return redirect(url_for('homepage.index'))
