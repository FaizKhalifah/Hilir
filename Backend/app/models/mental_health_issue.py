from app.models.base import BaseModel
from app.utils.db import db

class MentalHealthIssue(BaseModel):
    __tablename__ = "mental_health_issues"
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    threshold_score = db.Column(db.Integer, nullable=False)

    # Back-populates for bidirectional relationship
    related_questions = db.relationship("QuestionMentalHealth", back_populates="mental_health_issue", lazy=True)