from app.models.base import BaseModel
from app.utils.db import db

class QuestionMentalHealth(BaseModel):
    __tablename__ = "question_mental_health"
    question_id = db.Column(db.Integer, db.ForeignKey("personalization_questions.id"), nullable=False)
    mental_health_issue_id = db.Column(db.Integer, db.ForeignKey("mental_health_issues.id"), nullable=False)
    score_impact = db.Column(db.Float, nullable=False)
    question = db.relationship("PersonalizationQuestion", backref="related_mental_health_issues", lazy=True)
    mental_health_issue = db.relationship("MentalHealthIssue", backref="related_questions", lazy=True)