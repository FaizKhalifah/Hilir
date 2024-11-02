from app.models.base import BaseModel
from app.utils.db import db
from datetime import time

class PsychologistSchedule(BaseModel):
    __tablename__ = "psychologist_schedules"
    
    psychologist_id = db.Column(db.Integer, db.ForeignKey("psychologists.id"), nullable=False)
    start_time = db.Column(db.Time, nullable=False)  # Start time of the available slot
    end_time = db.Column(db.Time, nullable=False)  # End time of the available slot
    is_available = db.Column(db.Boolean, default=True)  # Whether the slot is available or not

    psychologist = db.relationship("Psychologist", backref="schedules", lazy=True)

    def check_availability(self, current_time):
        """Check if the psychologist is available at a specific time today."""
        return self.start_time <= current_time < self.end_time and self.is_available
