# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from app.config import Config
from app.utils.db import init_db
from app.controllers.parent_controller import parent_bp
from app.seed_cli import seed  # Import the CLI command from seed_cli.py

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)

    # Initialize mail
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(parent_bp, url_prefix="/api/parents")

    # Register the CLI command
    app.cli.add_command(seed)

    return app
