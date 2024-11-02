from app.repositories.psychologist_repository import PsychologistRepository
from app.repositories.child_repository import ChildRepository
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
    def get_all_psychologists():
        return PsychologistRepository.get_all_psychologists()

    @staticmethod
    def get_psychologist_detail(psychologist_id):
        return PsychologistRepository.get_psychologist_by_id(psychologist_id)
    @staticmethod
    def get_all_children_for_psychologist(psychologist_id):
        """Retrieve all children associated with a paid consultation for a specific psychologist."""
        # Get child IDs from consultations
        child_ids = PsychologistRepository.get_child_ids_with_paid_consultations(psychologist_id)
        
        # Retrieve child details for each associated child
        children = []
        for child_id in child_ids:
            child = ChildRepository.get_child_details(child_id)
            if child:
                # Prepare structured child data
                child_data = {
                    "child_id": child.id,
                    "name": child.name,
                    "age": child.age,
                    "gender": child.gender
                }
                children.append(child_data)
                
        return children

    @staticmethod
    def get_child_detail_for_psychologist(psychologist_id, child_id):
        """Get specific child detail for a psychologist with paid consultations."""
        return PsychologistRepository.get_child_detail_for_psychologist(psychologist_id, child_id)
    @staticmethod
    def get_child_mental_health_report_for_psychologist(psychologist_id, child_id):
        """Get detailed mental health report for a child, if associated with a paid consultation for the psychologist."""
        # Ensure the child is associated with a paid consultation for the psychologist
        consultation = PsychologistRepository.get_paid_consultation_for_child(psychologist_id, child_id)
        if not consultation:
            return None, "Access denied or child not found."

        # Retrieve child details
        child = ChildRepository.get_child_details(child_id)
        if not child:
            return None, "Child not found."

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