from app.models.base import BaseModel
from app.utils.db import db

class PsychologistSchedule(BaseModel):
    __tablename__ = "psychologist_schedules"
    psychologist_id = db.Column(db.Integer, db.ForeignKey("psychologists.id"), nullable=False)
    schedule_date = db.Column(db.Date, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    psychologist = db.relationship("Psychologist", backref="schedules", lazy=True)
