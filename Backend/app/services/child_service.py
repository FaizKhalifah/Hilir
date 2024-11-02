# app/services/child_service.py

from app.repositories.child_repository import ChildRepository

from app.repositories.child_repository import ChildRepository
from app.models.child import Child
from app.models.consultation import Consultation
from app.utils.db import db
from app.models.child_personalization import ChildPersonalization
from app.repositories.exercise_repository import ExerciseRepository
from app.models.child_exercise import ChildExercise
from app.models.mental_health_issue import MentalHealthIssue
from app.models.assessment import Assessment
from app.repositories.question_repository import QuestionRepository

class ChildService:
    @staticmethod
    def create_child(parent_id, data):
        return ChildRepository.create_child(parent_id, data)

    @staticmethod
    def get_all_children(parent_id):
        return ChildRepository.get_all_children(parent_id)

    @staticmethod
    def get_child_detail(parent_id, child_id):
        return ChildRepository.get_child_detail(parent_id, child_id)

    def get_child_mental_health_report(child_id):
        # Retrieve child details
        child = ChildRepository.get_child_details(child_id)
        if not child:
            return None, "Child not found"

        # Retrieve mental health scores
        scores = ChildRepository.get_child_personalization_scores(child_id)
        
        # Prepare structured report data
        report = {
            "child_id": child.id,
            "name": child.name,
            "age": child.age,
            "gender": child.gender,
            "mental_health_scores": []
        }

        # Populate scores and identify if they exceed thresholds
        for score in scores:
            issue = score.mental_health_issue
            report["mental_health_scores"].append({
                "issue_name": issue.name,
                "score": score.personalization_score,
                "threshold": issue.threshold_score,
                "exceeds_threshold": score.personalization_score >= issue.threshold_score
            })

        return report, None
    
    def is_child_owned_by_parent(child_id, parent_id):
        """Check if the given child belongs to the specified parent."""
        child = Child.query.filter_by(id=child_id, parent_id=parent_id).first()
        return child is not None

    @staticmethod
    def get_children_for_psychologist(psychologist_id):
        """Get a list of children who have had paid consultations with a specific psychologist."""
        consultations = (
            db.session.query(Child, Consultation)
            .join(Consultation, Consultation.child_id == Child.id)
            .filter(Consultation.psychologist_id == psychologist_id, Consultation.is_paid == True)
            .all()
        )
        return consultations

    @staticmethod
    def get_child_detail_for_psychologist(child_id, psychologist_id):
        """Get details of a specific child if there is a paid consultation with a psychologist."""
        consultation = (
            db.session.query(Child, Consultation)
            .join(Consultation, Consultation.child_id == Child.id)
            .filter(Consultation.child_id == child_id, 
                    Consultation.psychologist_id == psychologist_id,
                    Consultation.is_paid == True)
            .first()
        )
        return consultation
    
    @staticmethod
    def get_available_exercises_for_child(child_id):
        # Step 1: Fetch mental health issues with exceeded thresholds for this child
        exceeded_issues = (
            db.session.query(ChildPersonalization)
            .join(MentalHealthIssue, ChildPersonalization.mental_health_issue_id == MentalHealthIssue.id)
            .filter(
                ChildPersonalization.child_id == child_id,
                ChildPersonalization.personalization_score >= MentalHealthIssue.threshold_score
            )
            .all()
        )

        if not exceeded_issues:
            return [], "No mental health issues exceeding thresholds found for this child"

        # Get the list of mental health issue IDs that exceeded thresholds
        exceeded_issue_ids = [issue.mental_health_issue_id for issue in exceeded_issues]

        # Step 2: Retrieve all exercises for these mental health issues
        exercises = ExerciseRepository.get_exercises_by_mental_health_issues(exceeded_issue_ids)

        # Step 3: Filter out exercises already assigned to this child (unless it's assigned to this specific child)
        assigned_exercise_ids = {
            ex.exercise_id for ex in ChildExercise.query.filter(
                ChildExercise.child_id != child_id,
                ChildExercise.exercise_id.in_([exercise.id for exercise in exercises])
            ).all()
        }

        # Filter exercises based on assignment exclusion
        available_exercises = [
            {
                "id": exercise.id,
                "title": exercise.title,
                "description": exercise.description
            }
            for exercise in exercises if exercise.id not in assigned_exercise_ids
        ]

        return available_exercises, None
    
    @staticmethod
    def complete_assessment_and_generate_questions(child_id, assessment_id):
        # Find the assessment and validate ownership and status
        assessment = Assessment.query.filter_by(id=assessment_id, child_id=child_id, is_completed=False).first()
        if not assessment:
            return None, None, "Assessment not found or already completed."

        # Mark assessment as completed
        assessment.is_completed = True
        db.session.commit()

        # Generate questions for the parent based on child’s mental health issues
        questions = QuestionRepository.get_questions_for_mental_health_issues(child_id)

        # Format questions for the response
        formatted_questions = [
            {"question_id": q.id, "question": q.question, "mental_health_issue_id": q.mental_health_issue_id}
            for q in questions
        ]

        return assessment, formatted_questions, None

    @staticmethod
    def apply_response_impact(child_id, question_id, response_score):
        """Apply score impacts to mental health issues based on response."""
        impacts = QuestionRepository.get_score_impacts(question_id)
        
        for impact in impacts:
            personalization = ChildPersonalization.query.filter_by(
                child_id=child_id,
                mental_health_issue_id=impact.mental_health_issue_id
            ).first()
            if personalization:
                personalization.personalization_score += impact.score_impact * response_score
                db.session.commit()