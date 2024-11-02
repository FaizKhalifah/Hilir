# app/services/psychologist_service.py

from app.repositories.psychologist_repository import PsychologistRepository
from app.repositories.child_repository import ChildRepository
from app.models.assessment import Assessment
from app.utils.db import db
from app.repositories.exercise_repository import ExerciseRepository
from app.models.personalization_question import PersonalizationQuestion
from app.models.question_mental_health import QuestionMentalHealth
from app.models.psychologist import Psychologist
from app.repositories.assessment_repository import AssessmentRepository
class PsychologistService:

    @staticmethod
    def register_psychologist(data):
        return PsychologistRepository.create_psychologist(data)

    @staticmethod
    def authenticate_psychologist(email, password):
        psychologist = PsychologistRepository.get_psychologist_by_email(email)
        if psychologist and psychologist.check_password(password):
            return psychologist
        return None

    @staticmethod
    def get_all_children_for_psychologist(psychologist_id):
        child_ids = PsychologistRepository.get_child_ids_with_paid_consultations(psychologist_id)
        children = [ChildRepository.get_child_details(child_id) for child_id in child_ids]
        return [
            {
                "child_id": child.id,
                "name": child.name,
                "age": child.age,
                "gender": child.gender
            } for child in children if child
        ]

    @staticmethod
    def get_child_mental_health_report_for_psychologist(psychologist_id, child_id):
        consultation = PsychologistRepository.get_paid_consultation_for_child(psychologist_id, child_id)
        if not consultation:
            return None, "Access denied or child not found."

        child = ChildRepository.get_child_details(child_id)
        if not child:
            return None, "Child not found."

        scores = ChildRepository.get_child_personalization_scores(child_id)
        report = {
            "child_id": child.id,
            "name": child.name,
            "age": child.age,
            "gender": child.gender,
            "mental_health_scores": []
        }

        for score in scores:
            issue = score.mental_health_issue
            report["mental_health_scores"].append({
                "issue_name": issue.name,
                "score": score.personalization_score,
                "threshold": issue.threshold_score,
                "exceeds_threshold": score.personalization_score >= issue.threshold_score
            })

        return report, None

    @staticmethod
    def add_and_assign_exercise_to_child(psychologist_id, child_id, exercise_data):
        return PsychologistRepository.add_and_assign_exercise_to_child(child_id, exercise_data, psychologist_id)

    @staticmethod
    def get_exercises_for_psychologist(psychologist_id):
        """Retrieve exercises based on the psychologist's specialization."""
        specialization_id = PsychologistRepository.get_specialization_id(psychologist_id)
        if not specialization_id:
            return None, "Specialization not recognized."
        
        exercises = PsychologistRepository.get_exercises_for_specialization(specialization_id)
        return [{"id": exercise.id, "title": exercise.title, "description": exercise.description} for exercise in exercises], None
    @staticmethod
    def add_assessment(psychologist_id, child_id, assessment_data):
        # Check if a paid consultation exists between the psychologist and child
        consultation = PsychologistRepository.get_paid_consultation_for_child(psychologist_id, child_id)
        if not consultation:
            return None, "Access denied: No paid consultation for this child."

        # Create and save new assessment
        assessment = Assessment(
            child_id=child_id,
            psychologist_id=psychologist_id,
            task_description=assessment_data["task_description"],
            due_date=assessment_data["due_date"],
            frequency=assessment_data["frequency"],  # Frequency in hours
            is_completed=False
        )
        db.session.add(assessment)
        db.session.commit()

        return assessment, None
    
    @staticmethod
    def add_assessment_with_questions(psychologist_id, child_id, assessment_data, questions):
        consultation = PsychologistRepository.get_paid_consultation_for_child(psychologist_id, child_id)
        if not consultation:
            return None, "Access denied: No paid consultation for this child."

        # Create the assessment
        assessment = Assessment(
            child_id=child_id,
            psychologist_id=psychologist_id,
            task_description=assessment_data["task_description"],
            due_date=assessment_data["due_date"],
            frequency=assessment_data["frequency"],
            is_completed=False
        )
        db.session.add(assessment)
        db.session.flush()

        # Add each question and associate with mental health impacts
        for question_data in questions:
            question = PersonalizationQuestion(
                assessment_id=assessment.id,
                question=question_data["question"]
            )
            db.session.add(question)
            db.session.flush()

            for impact in question_data["impacts"]:
                question_impact = QuestionMentalHealth(
                    question_id=question.id,
                    mental_health_issue_id=impact["mental_health_issue_id"],
                    score_impact=impact["score_impact"]
                )
                db.session.add(question_impact)

        db.session.commit()
        return assessment, None
    @staticmethod
    def get_all_psychologists():
        return Psychologist.query.all()
    
    @staticmethod
    def get_psychologist_details(psychologist_id):
        """Get the details of a specific psychologist by their ID."""
        psychologist = PsychologistRepository.get_psychologist_by_id(psychologist_id)
        if not psychologist:
            return None, "Psychologist not found"

        # Get today's schedule for the psychologist
        schedules = PsychologistRepository.get_schedule_for_today(psychologist_id)
        schedule_data = [
            {
                "start_time": str(schedule.start_time),
                "end_time": str(schedule.end_time),
                "is_available": schedule.is_available
            } for schedule in schedules
        ]

        return {
            "id": psychologist.id,
            "full_name": psychologist.full_name,
            "email": psychologist.email,
            "specialization": psychologist.specialization,
            "bio": psychologist.bio,
            "today_schedule": schedule_data
        }, None
    @staticmethod
    def get_all_assessments(psychologist_id):
        """Get all assessments associated with a specific psychologist."""
        assessments = AssessmentRepository.get_all_assessments_for_psychologist(psychologist_id)
        
        if not assessments:
            return None, "No assessments found for this psychologist."
        
        # Prepare a list of assessments for response
        assessments_data = [
            {
                "id": assessment.id,
                "child_id": assessment.child_id,
                "task_description": assessment.task_description,
                "due_date": str(assessment.due_date),
                "frequency": assessment.frequency,
                "is_completed": assessment.is_completed
            } for assessment in assessments
        ]
        
        return assessments_data, None
    
    @staticmethod
    def get_schedule_for_psychologist(psychologist_id, requested_date):
        """Get the schedule for a specific psychologist by their ID for a specific date."""
        schedules = PsychologistRepository.get_schedule_for_psychologist(psychologist_id)
        if not schedules:
            return None, "No schedules found for this psychologist."

        # Check if there are available slots for the requested date
        available_slots = PsychologistRepository.get_available_slots_for_date(psychologist_id, requested_date)
        is_available_on_date = len(available_slots) > 0

        # Format the schedules for response
        schedule_data = [
            {
                "start_time": str(schedule.start_time),
                "end_time": str(schedule.end_time),
                "is_available": schedule.is_available
            } for schedule in schedules
        ]

        response = {
            "schedule": schedule_data,
            "available_on_date": is_available_on_date
        }
        
        return response, None