from app.repositories.consultation_repository import ConsultationRepository
from app.models.consultation import Consultation
from app.utils.db import db
from datetime import datetime

class ConsultationService:
    @staticmethod
    def book_consultation(child_id, psychologist_id, consultation_date, start_time, end_time):
        available = ConsultationRepository.is_psychologist_available(
            psychologist_id=psychologist_id,
            consultation_date=consultation_date,
            start_time=start_time,
            end_time=end_time
        )

        if not available:
            return None, "Psychologist is not available at the selected time."

        consultation = Consultation(
            child_id=child_id,
            psychologist_id=psychologist_id,
            consultation_date=datetime.strptime(consultation_date, "%Y-%m-%d").date(),
            start_time=datetime.strptime(start_time, "%H:%M").time(),
            end_time=datetime.strptime(end_time, "%H:%M").time(),
            is_paid=True
        )

        try:
            db.session.add(consultation)
            db.session.commit()
            return consultation, None
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to book consultation: {str(e)}"
