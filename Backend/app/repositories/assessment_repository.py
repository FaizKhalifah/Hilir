from app.utils.db import db
from app.models.assessment import Assessment

class AssessmentRepository:
    @staticmethod
    def get_all_assessments_for_psychologist(psychologist_id):
        return Assessment.query.filter_by(psychologist_id=psychologist_id).all()
