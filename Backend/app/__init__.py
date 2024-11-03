from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from app.config import Config
from app.utils.db import init_db
from app.routes.parent_routes import parent_bp 
from app.routes.psychologist_routes import psychologist_bp 

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app) 

    CORS(app)
    mail.init_app(app) 
    app.register_blueprint(parent_bp, url_prefix="/api/parents")
    app.register_blueprint(psychologist_bp, url_prefix="/api/psychologists")

    return app
