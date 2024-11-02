# app/services/child_service.py

from app.repositories.child_repository import ChildRepository

from app.repositories.child_repository import ChildRepository
from app.models.child import Child
from app.models.consultation import Consultation
from app.utils.db import db

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