# app/repositories/psychologist_repository.py

from app.utils.db import db
from app.models.psychologist import Psychologist
from app.models.child import Child
from app.models.consultation import Consultation
from app.models.child_exercise import ChildExercise
from app.models.exercise import Exercise
from datetime import datetime

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
    def get_specialization_id(psychologist_id):
        """Map psychologist specialization to mental health issue ID."""
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
        """Retrieve exercises based on a specific mental health issue ID."""
        return Exercise.query.filter_by(mental_health_issue_id=mental_health_issue_id).all()

    @staticmethod
    def add_and_assign_exercise_to_child(child_id, exercise_data, psychologist_id):
        # Ensure the psychologist has a paid consultation with the child
        consultation = db.session.query(Consultation).filter_by(
            psychologist_id=psychologist_id, child_id=child_id, is_paid=True
        ).first()
        
        if not consultation:
            return None, "Access denied: No paid consultation for this child."

        # Create a new exercise
        new_exercise = Exercise(
            title=exercise_data["title"],
            description=exercise_data.get("description"),
            mental_health_issue_id=exercise_data["mental_health_issue_id"]
        )
        db.session.add(new_exercise)
        db.session.flush()  # Get the exercise ID immediately after insertion

        # Assign the new exercise to the child
        child_exercise = ChildExercise(
            child_id=child_id,
            exercise_id=new_exercise.id,
            assigned_date=exercise_data["assigned_date"],
            is_completed=False
        )
        db.session.add(child_exercise)
        db.session.commit()

        return child_exercise, None
