
import click
from flask.cli import with_appcontext
from app.seeds import seed_database
from app.utils.db import db


@click.command(name='seed')
@with_appcontext
def seed():
    """Seed the database with initial data."""
    db.drop_all()
    db.create_all()
    seed_database()