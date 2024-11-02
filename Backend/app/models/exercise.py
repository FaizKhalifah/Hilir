from app.models.base import BaseModel
from app.utils.db import db

class Exercise(BaseModel):
    __tablename__ = "exercises"
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    mental_health_issue_id = db.Column(db.Integer, db.ForeignKey("mental_health_issues.id"), nullable=False)

    mental_health_issue = db.relationship("MentalHealthIssue", backref="exercises", lazy=True)
