from urllib.parse import urljoin
from urllib.parse import urlparse

from app import db
from app.blueprints.email import send_password_reset_email
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import ResetPasswordForm
from app.forms import ResetPasswordRequestForm
from app.models import User
from flask import abort 
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

bp = Blueprint("auth", __name__, url_prefix="/auth")


def _is_safe_url(target):
    host_url = urlparse(request.host_url)
    next_url = urlparse(urljoin(request.host_url, target))
    return next_url.scheme in ("http", "https") and host_url.netloc == next_url.netloc


@bp.route("/register/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have been registered!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@bp.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect(url_for("homepage.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not _is_safe_url(next_page):
            return abort(400)
        return redirect(next_page or url_for("homepage.index"))
    return render_template("auth/login.html", form=form)


@bp.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/recover/", methods=["GET", "POST"])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password")
    return render_template("auth/password_reset_request.html", form=form)


@bp.route("/reset/<token>/", methods=["GET", "POST"])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        flash("Invalid recovery token")
        return redirect(url_for("homepage.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("homepage.index"))
    return render_template("email/password_reset_form.html", form=form)
