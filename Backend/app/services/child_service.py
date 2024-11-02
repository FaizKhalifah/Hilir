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
from app.utils.gemini_api import GeminiAPI
from app.utils.parse_utils import parse_exercises
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
    
    @staticmethod
    def _generate_prompt(exceeded_issues):
        """
        Updated prompt generator with more consistent formatting instructions.
        """
        issues_list = ", ".join([f"Mental health issue {issue['id']} ({issue['name']})" for issue in exceeded_issues])
        issue_count = len(exceeded_issues)
        
        base_prompt = (
            f"Create {issue_count} {'exercise' if issue_count == 1 else 'exercises'} for an 8-year-old child with {issues_list}. "
            "Format each exercise exactly like this:\n\n"
            "**Title**: [Exercise Name]\n"
            "**Description**: [Clear step-by-step instructions]\n"
            "**Mental_health_issue_id**: [Issue ID]\n\n"
            "Use these IDs: 7 for ADHD, 8 for autism, 9 for anxiety.\n\n"
            "Important formatting rules:\n"
            "1. Start each exercise with **Title**\n"
            "2. Include all three fields for each exercise\n"
            "3. Separate exercises with a blank line\n"
            "4. Make sure each exercise matches one of the child's issues\n\n"
        )
        
        # Add example based on number of exercises needed
        example = (
            "Example format:\n"
            "**Title**: Calm Down Corner\n"
            "**Description**: Create a quiet space with soft pillows and calming toys. "
            "Child can go here when feeling overwhelmed to practice deep breathing.\n"
            "**Mental_health_issue_id**: 9\n\n"
        )
        
        if issue_count > 1:
            example += (
                "**Title**: Focus Time\n"
                "**Description**: Use a visual timer for homework. Break work into 10-minute chunks "
                "with short breaks in between.\n"
                "**Mental_health_issue_id**: 7\n\n"
            )
        
        return base_prompt + example + f"Now please create {issue_count} new {'exercise' if issue_count == 1 else 'exercises'}."

    @staticmethod
    def assign_exercises_based_on_issues(child_id):
        child_personalizations = ChildRepository.get_child_personalizations(child_id)
        exceeded_issues = [
            {"id": personalization.mental_health_issue_id, "name": personalization.mental_health_issue.name}
            for personalization in child_personalizations
            if personalization.personalization_score >= personalization.mental_health_issue.threshold_score
        ]

        if not exceeded_issues:
            return None, "No mental health issues exceed the threshold for additional exercises."

        # Generate prompt and get response
        prompt = ChildService._generate_prompt(exceeded_issues)
        response_json, error = GeminiAPI.get_exercises_for_prompt(prompt)
        
        if error:
            return None, f"Failed to fetch exercises from Gemini API: {error}"

        # Parse exercises with improved parser
        exercises = parse_exercises(response_json)

        # Validate number of exercises
        if not exercises:
            return None, "No valid exercises could be parsed from the response."
        
        if len(exercises) != len(exceeded_issues):
            # Try to salvage what we can if we got some exercises
            if exercises:
                print(f"Warning: Expected {len(exceeded_issues)} exercises, but received {len(exercises)}. Proceeding with available exercises.")
            else:
                return None, f"Expected {len(exceeded_issues)} exercises, but received {len(exercises)}."

        # Save valid exercises to the child
        for exercise_data in exercises:
            exercise = ExerciseRepository.create_exercise(
                title=exercise_data["title"],
                description=exercise_data["description"],
                mental_health_issue_id=exercise_data["mental_health_issue_id"]
            )
            ExerciseRepository.assign_exercise_to_child(child_id, exercise.id)

        return exercises, None
    @staticmethod
    def get_child_exercises(child_id):
        """
        Get all exercises assigned to a child with their completion status.
        """
        child_exercises = ExerciseRepository.get_child_exercises(child_id)
        return [{
            "exercise_id": ce.exercise_id,
            "title": ce.exercise.title,
            "description": ce.exercise.description,
            "assigned_date": ce.assigned_date.isoformat(),
            "is_completed": ce.is_completed,
            "mental_health_issue_id": ce.exercise.mental_health_issue_id
        } for ce in child_exercises]

    @staticmethod
    def mark_exercise_complete(child_id, exercise_id):
        """
        Mark an exercise as completed for a child.
        """
        child_exercise = ChildExercise.query.filter_by(
            child_id=child_id,
            exercise_id=exercise_id
        ).first()
        
        if child_exercise:
            child_exercise.is_completed = True
            db.session.commit()
            return True
        return False