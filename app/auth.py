from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.email import send_password_reset_email
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register/', methods=['POST'])
def register():
    if current_user.is_authenticated:
        flash("You already have an active account")
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('You have been registered!')
    return redirect(url_for('homepage.index'))


@bp.route('/login/', methods=['POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in")
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('homepage.index'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page and url_parse(next_page).netloc == '':
                return redirect(next_page)
    return redirect(url_for('homepage.index'))


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage.index'))


@bp.route('/recover/', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        flash('Password recovery is only possible for non-authenticated users')
    else:
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
    return redirect(url_for('homepage.index'))


@bp.route('/reset/<token>/', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('homepage.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('homepage.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('homepage.index'))
    return render_template('email/password_reset_form.html', form=form)

