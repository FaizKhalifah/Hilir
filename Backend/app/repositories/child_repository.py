# app/repositories/child_repository.py

from app.models.child import Child
from app.utils.db import db
from app.models.child_personalization import ChildPersonalization
from app.models.child_exercise import ChildExercise
from app.models.exercise import Exercise

class ChildRepository:
    @staticmethod
    def create_child(parent_id, data):
        child = Child(parent_id=parent_id, **data)
        db.session.add(child)
        db.session.commit()
        return child

    @staticmethod
    def get_all_children(parent_id):
        return Child.query.filter_by(parent_id=parent_id).all()

    @staticmethod
    def get_child_details(child_id):
        # Retrieve basic child details
        return Child.query.get(child_id)

    @staticmethod
    def get_child_personalization_scores(child_id):
        # Retrieve scores for each mental health issue linked to the child
        scores = ChildPersonalization.query.filter_by(child_id=child_id).all()
        return scores

    @staticmethod
    def get_exercises_by_mental_health_issues(mental_health_issue_ids):
        return Exercise.query.filter(Exercise.mental_health_issue_id.in_(mental_health_issue_ids)).all()
    
    def get_child_personalizations(child_id):
        return ChildPersonalization.query.filter_by(child_id=child_id).all()