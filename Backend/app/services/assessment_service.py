from app.models.assessment import Assessment
from app.utils.db import db
from datetime import date, timedelta

class AssessmentService:
    @staticmethod
    def generate_assessment_prompts(mental_health_issues):
        prompts = []
        for issue in mental_health_issues[:3]:
            prompts.append(
                f"Create an assessment task description for a child with {issue['name']} "
                "that is age-appropriate for an 8-year-old. "
                "The task should help manage symptoms and be easy to understand.\n\n"
                "Format:\n\n"
                "**Task Description**: [Detailed instructions]\n"
            )
        return prompts

    @staticmethod
    def create_assessment_for_child(child_id, task_description, days_to_complete):
        try:
            assessment = Assessment(
                child_id=child_id,
                task_description=task_description,
                days_to_complete=days_to_complete,
                frequency=1
            )
            
            db.session.add(assessment)
            db.session.commit()
            return assessment, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
