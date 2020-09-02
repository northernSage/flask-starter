from app import mail
from flask import Blueprint
from flask import current_app
from flask import render_template
from flask_mail import Message

bp = Blueprint("email", __name__)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        "Reset Your Password",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[user.email],
        text_body=render_template(
            "email/reset_password_email.txt", user=user, token=token
        ),
        html_body=render_template(
            "email/reset_password_email.html", user=user, token=token
        ),
    )
