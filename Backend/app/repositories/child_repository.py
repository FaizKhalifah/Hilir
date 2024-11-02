# app/repositories/child_repository.py

from app.models.child import Child
from app.utils.db import db
from app.models.child_personalization import ChildPersonalization

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
