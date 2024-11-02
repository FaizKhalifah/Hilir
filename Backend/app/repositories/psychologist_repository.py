from app.utils.db import db
from app.models.psychologist import Psychologist
from app.models.child import Child
from app.models.consultation import Consultation
from app.models.child_exercise import ChildExercise
from app.models.exercise import Exercise
from datetime import datetime
from app.models.psychologist_schedule import PsychologistSchedule
from datetime import date

class PsychologistRepository:
    @staticmethod
    def create_psychologist(data):
        psychologist = Psychologist(
            full_name=data["full_name"],
            email=data["email"],
            specialization=data["specialization"],
            bio=data.get("bio", "")
        )
        psychologist.set_password(data["password"])
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
    def get_specialization_id(psychologist_id):
        psychologist = Psychologist.query.get(psychologist_id)
        if not psychologist:
            return None
        specialization_map = {
            "ADHD": 1,
            "Autism": 2,
            "Anxiety": 3
        }
        return specialization_map.get(psychologist.specialization)

    @staticmethod
    def get_exercises_for_specialization(mental_health_issue_id):
        return Exercise.query.filter_by(mental_health_issue_id=mental_health_issue_id).all()

    @staticmethod
    def add_and_assign_exercise_to_child(child_id, exercise_data, psychologist_id):
        consultation = db.session.query(Consultation).filter_by(
            psychologist_id=psychologist_id, child_id=child_id, is_paid=True
        ).first()
        
        if not consultation:
            return None, "Access denied: No paid consultation for this child."

        new_exercise = Exercise(
            title=exercise_data["title"],
            description=exercise_data.get("description"),
            mental_health_issue_id=exercise_data["mental_health_issue_id"]
        )
        db.session.add(new_exercise)
        db.session.flush()

        child_exercise = ChildExercise(
            child_id=child_id,
            exercise_id=new_exercise.id,
            assigned_date=exercise_data["assigned_date"],
            is_completed=False
        )
        db.session.add(child_exercise)
        db.session.commit()

        return child_exercise, None
    
    @staticmethod
    def get_paid_consultation_for_child(psychologist_id, child_id):
        return Consultation.query.filter_by(
            psychologist_id=psychologist_id,
            child_id=child_id,
            is_paid=True
        ).first()
    
    @staticmethod
    def get_child_ids_with_paid_consultations(psychologist_id):
        consultations = Consultation.query.filter_by(psychologist_id=psychologist_id, is_paid=True).all()
        return [consultation.child_id for consultation in consultations]
    
    @staticmethod
    def get_psychologist_by_id(psychologist_id):
        return Psychologist.query.get(psychologist_id)

    @staticmethod
    def get_schedule_for_today(psychologist_id):
        return PsychologistSchedule.query.filter_by(
            psychologist_id=psychologist_id,
            is_available=True
        ).all()
    
    @staticmethod
    def get_schedule_for_psychologist(psychologist_id):
        return PsychologistSchedule.query.filter_by(psychologist_id=psychologist_id).all()

    @staticmethod
    def get_available_slots_for_date(psychologist_id, requested_date):
        schedules = PsychologistSchedule.query.filter_by(psychologist_id=psychologist_id, is_available=True).all()
    
        if requested_date == datetime.now().date():
            current_time = datetime.now().time()
            available_on_requested_date = [
                schedule for schedule in schedules if schedule.start_time > current_time
            ]
        else:
            available_on_requested_date = schedules

        return available_on_requested_date
