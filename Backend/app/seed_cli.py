# app/seed_cli.py

import click
from flask.cli import with_appcontext
from app.seeds import seed_questions

@click.command("seed_questions")
@with_appcontext
def seed():
    """Seed the database with questions and mental health issues."""
    seed_questions()
    print("Seeded questions and mental health issues successfully.")
