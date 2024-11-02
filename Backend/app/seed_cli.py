# app/seed_cli.py

import click
from flask.cli import with_appcontext
from app.seeds import run_seeds

@click.command("seed_database")
@with_appcontext
def seed():
    """Seed the database with psychologists, schedules, and consultations."""
    run_seeds()
    print("Database seeded successfully.")
