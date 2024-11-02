from app.models.base import BaseModel
from app.utils.db import db

class MentalHealthIssue(BaseModel):
    __tablename__ = "mental_health_issues"
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    threshold_score = db.Column(db.Integer, nullable=False)
