from app.models.base import BaseModel
from app.utils.db import db

class Consultation(BaseModel):
    __tablename__ = "consultations"
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    psychologist_id = db.Column(db.Integer, db.ForeignKey("psychologists.id"), nullable=False)
    consultation_date = db.Column(db.Date, nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)

    child = db.relationship("Child", backref="consultations", lazy=True)
    psychologist = db.relationship("Psychologist", backref="consultations", lazy=True)
