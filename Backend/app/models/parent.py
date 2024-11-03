from app.utils.db import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class Parent(BaseModel):
    __tablename__ = "parents"

    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
