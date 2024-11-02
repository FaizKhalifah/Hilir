from app.models.exercise import Exercise
from app.models.child_exercise import ChildExercise
from app.utils.db import db
class ExerciseRepository:

    @staticmethod
    def get_exercises_by_mental_health_issue(mental_health_issue_id):
        return Exercise.query.filter_by(mental_health_issue_id=mental_health_issue_id).all()

    @staticmethod
    def get_exercises_by_mental_health_issues(mental_health_issue_ids):
        """Retrieve all exercises associated with a list of mental health issue IDs."""
        return Exercise.query.filter(Exercise.mental_health_issue_id.in_(mental_health_issue_ids)).all()
    
    @staticmethod
    def create_exercise(title, description, mental_health_issue_id):
        exercise = Exercise(
            title=title,
            description=description,
            mental_health_issue_id=mental_health_issue_id
        )
        db.session.add(exercise)
        db.session.commit()
        return exercise

    @staticmethod
    def assign_exercise_to_child(child_id, exercise_id):
        child_exercise = ChildExercise(
            child_id=child_id,
            exercise_id=exercise_id,
            assigned_date=db.func.current_date(),
            is_completed=False
        )
        db.session.add(child_exercise)
        db.session.commit()
