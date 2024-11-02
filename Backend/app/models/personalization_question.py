from app.models.base import BaseModel
from app.utils.db import db

class PersonalizationQuestion(BaseModel):
    __tablename__ = "personalization_questions"
    question = db.Column(db.String, nullable=False)
