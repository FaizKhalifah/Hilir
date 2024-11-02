# app/models/psychologist.py

from app.utils.db import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class Psychologist(BaseModel):
    __tablename__ = "psychologists"

    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    specialization = db.Column(db.String, nullable=False)
    bio = db.Column(db.Text, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
