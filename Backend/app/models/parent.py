from app.models.base import BaseModel
from app.utils.db import db

class Parent(BaseModel):
    __tablename__ = "parents"
    
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
