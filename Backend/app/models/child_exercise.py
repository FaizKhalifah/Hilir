from app.models.base import BaseModel
from app.utils.db import db

class ChildExercise(BaseModel):
    __tablename__ = "child_exercises"
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

    child = db.relationship("Child", backref="child_exercises", lazy=True)
    exercise = db.relationship("Exercise", backref="child_exercises", lazy=True)
