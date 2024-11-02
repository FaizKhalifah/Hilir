# app/repositories/psychologist_repository.py

from app.utils.db import db
from app.models.psychologist import Psychologist

class PsychologistRepository:

    @staticmethod
    def create_psychologist(data):
        psychologist = Psychologist(
            full_name=data["full_name"],
            email=data["email"],
            specialization=data["specialization"],
            bio=data.get("bio", "")
        )
        psychologist.set_password(data["password"])  # Hash the password
        db.session.add(psychologist)
        db.session.commit()
        return psychologist

    @staticmethod
    def get_psychologist_by_email(email):
        return Psychologist.query.filter_by(email=email).first()
