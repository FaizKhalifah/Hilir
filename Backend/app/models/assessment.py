from app.models.base import BaseModel
from app.utils.db import db
from datetime import date, timedelta

class Assessment(BaseModel):
    __tablename__ = "assessments"

    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    psychologist_id = db.Column(db.Integer, db.ForeignKey("psychologists.id"), nullable=False)
    task_description = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    frequency = db.Column(db.Integer, nullable=False)

    child = db.relationship("Child", backref="assessments", lazy=True)
    psychologist = db.relationship("Psychologist", backref="assessments", lazy=True)
    questions = db.relationship("PersonalizationQuestion", backref="assessment", lazy=True)

    def __init__(self, child_id, task_description, days_to_complete, frequency=1):
        self.child_id = child_id
        self.psychologist_id = 9999
        self.task_description = task_description
        self.due_date = date.today() + timedelta(days=days_to_complete)
        self.is_completed = False
        self.frequency = frequency
