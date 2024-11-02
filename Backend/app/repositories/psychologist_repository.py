# app/repositories/psychologist_repository.py

from app.utils.db import db
from app.models.psychologist import Psychologist
from app.models.child import Child
from app.models.consultation import Consultation


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

    @staticmethod
    def get_all_psychologists():
        return Psychologist.query.all()

    @staticmethod
    def get_psychologist_by_id(psychologist_id):
        return Psychologist.query.filter_by(id=psychologist_id).first()
    

    @staticmethod
    def get_child_ids_with_paid_consultations(psychologist_id):
        """Fetch child IDs that have paid consultations with the specified psychologist."""
        consultations = db.session.query(Consultation.child_id).filter_by(
            psychologist_id=psychologist_id,
            is_paid=True
        ).distinct().all()
        
        return [consultation.child_id for consultation in consultations]

    @staticmethod
    def get_child_detail_for_psychologist(psychologist_id, child_id):
        """Fetch specific child details if associated with a paid consultation for the psychologist."""
        child = db.session.query(Child).join(Consultation).filter(
            Consultation.psychologist_id == psychologist_id,
            Consultation.child_id == child_id,
            Consultation.is_paid == True
        ).first()
        return child
    @staticmethod
    def get_paid_consultation_for_child(psychologist_id, child_id):
        """Check if there is a paid consultation between the psychologist and the child."""
        return db.session.query(Consultation).filter_by(
            psychologist_id=psychologist_id,
            child_id=child_id,
            is_paid=True
        ).first()