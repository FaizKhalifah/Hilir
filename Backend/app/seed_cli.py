# app/seed_cli.py

import click
from flask.cli import with_appcontext
from app.seeds import seed_exercises  # Import only the exercises seeding function

@click.command("seed_exercises")
@with_appcontext
def seed_exercises_command():
    """Seed the database with exercises only."""
    seed_exercises()
    print("Exercise data seeded successfully.")
