from setuptools import setup

setup(
    name="flask-starter",
    version="0.1.1",
    install_requires=[
        "flask",
        "flask-login",
        "flask-mail",
        "flask-migrate",
        "flask-sqlalchemy",
        "flask-wtf",
        "gunicorn",
        "jwt",
        "pytest",
        "redis",
        "rq",
        "pip-tools",
        "pre-commit",
        "email_validator",
    ],
)
