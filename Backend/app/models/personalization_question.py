from app.models.base import BaseModel
from app.utils.db import db

class PersonalizationQuestion(BaseModel):
    __tablename__ = "personalization_questions"
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)
    question = db.Column(db.String, nullable=False)

    related_mental_health_issues = db.relationship("QuestionMentalHealth", back_populates="personalization_question", lazy=True)
