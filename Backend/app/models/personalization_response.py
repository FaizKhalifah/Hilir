from app.models.base import BaseModel
from app.utils.db import db

class PersonalizationResponse(BaseModel):
    __tablename__ = "personalization_responses"
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("personalization_questions.id"), nullable=False)
    response_score = db.Column(db.Integer, nullable=False)

    child = db.relationship("Child", backref="personalization_responses", lazy=True)
    question = db.relationship("PersonalizationQuestion", backref="responses", lazy=True)
