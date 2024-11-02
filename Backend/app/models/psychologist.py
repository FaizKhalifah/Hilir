from app.models.base import BaseModel
from app.utils.db import db

class Psychologist(BaseModel):
    __tablename__ = "psychologists"
    name = db.Column(db.String, nullable=False)
    specialization = db.Column(db.String, nullable=True)
    education_background = db.Column(db.String, nullable=True)
    license_number = db.Column(db.String, nullable=False, unique=True)
