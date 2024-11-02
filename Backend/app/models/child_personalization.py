from app.models.base import BaseModel
from app.utils.db import db

class ChildPersonalization(BaseModel):
    __tablename__ = "child_personalizations"
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    mental_health_issue_id = db.Column(db.Integer, db.ForeignKey("mental_health_issues.id"), nullable=False)
    personalization_score = db.Column(db.Integer, nullable=False)

    child = db.relationship("Child", backref="personalizations", lazy=True)
    mental_health_issue = db.relationship("MentalHealthIssue", backref="child_personalizations", lazy=True)
