from app.models.exercise import Exercise
from app.models.child_exercise import ChildExercise
from app.utils.db import db
from datetime import date
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
    @staticmethod
    def create_exercise_with_child(title, description, mental_health_issue_id, child_id):
        """
        Create an exercise and immediately associate it with a child.
        """
        try:
            # Create the exercise
            exercise = Exercise(
                title=title,
                description=description,
                mental_health_issue_id=mental_health_issue_id
            )
            db.session.add(exercise)
            db.session.flush()  # Get the exercise ID before committing
            
            # Create the child-exercise association
            child_exercise = ChildExercise(
                child_id=child_id,
                exercise_id=exercise.id,
                assigned_date=date.today(),
                is_completed=False
            )
            db.session.add(child_exercise)
            db.session.commit()
            
            return exercise, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_child_exercises(child_id):
        """
        Get all exercises assigned to a child.
        """
        return ChildExercise.query.filter_by(child_id=child_id).all()