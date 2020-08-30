import click

from app import db
from app.models import User


def register(app):
    @app.cli.command('init-db')
    def init_db():
        """Initialize db"""
        click.echo("Initializing database...")
        db.create_all()
        click.echo("Done")

    @app.cli.command('nuke-db')
    def nuke_db():
        """Drop and recreate db"""
        click.echo('Droping db tables...')
        db.drop_all()
        click.echo('Done')
        db.create_all()
        click.echo('Creating db tables...')
        db.session.commit()
        click.echo('Done')

    @app.cli.command('create-test-user')
    def create_test_user():
        """Create a test user"""
        click.echo("Creating test user...")
        user = User(username='appuser', email='appuser@gmail.com')
        user.set_password('appuser')
        db.session.add(user)
        db.session.commit()
        click.echo("Done")
