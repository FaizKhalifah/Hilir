# app/services/psychologist_service.py

from app.repositories.psychologist_repository import PsychologistRepository
from app.repositories.child_repository import ChildRepository
from app.models.assessment import Assessment
from app.utils.db import db
from app.repositories.exercise_repository import ExerciseRepository

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