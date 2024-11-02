from app.models.exercise import Exercise

class ExerciseRepository:

    @staticmethod
    def get_exercises_by_mental_health_issue(mental_health_issue_id):
        return Exercise.query.filter_by(mental_health_issue_id=mental_health_issue_id).all()

    @staticmethod
    def get_exercises_by_mental_health_issues(mental_health_issue_ids):
        """Retrieve all exercises associated with a list of mental health issue IDs."""
        return Exercise.query.filter(Exercise.mental_health_issue_id.in_(mental_health_issue_ids)).all()
