from app.models.base import BaseModel
from app.utils.db import db

class Child(BaseModel):
    __tablename__ = "children"
    parent_id = db.Column(db.Integer, db.ForeignKey("parents.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String, nullable=True)

    parent = db.relationship("Parent", backref="children", lazy=True)
