from app.models.base import BaseModel
from app.utils.db import db

class PersonalizationQuestion(BaseModel):
    __tablename__ = "personalization_questions"
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)
    question = db.Column(db.String, nullable=False)
    question_mental_health = db.relationship("QuestionMentalHealth", backref="personalization_question", lazy=True)
