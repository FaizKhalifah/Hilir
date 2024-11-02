# app/models/parent.py

from app.utils.db import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class Parent(BaseModel):
    __tablename__ = "parents"

    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)  # Renamed from password_hash
    is_verified = db.Column(db.Boolean, default=False)  # New attribute for verification status

    def set_password(self, password):
        """Hashes the password and stores it in the password field."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifies a plaintext password against the hashed password."""
        return check_password_hash(self.password, password)
