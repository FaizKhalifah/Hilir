# app/repositories/consultation_repository.py

from app.models.consultation import Consultation
from app.models.psychologist_schedule import PsychologistSchedule
from app.utils.db import db
from datetime import datetime

class ConsultationRepository:
    @staticmethod
    def is_psychologist_available(psychologist_id, consultation_date, start_time, end_time):
        # Convert inputs to datetime for comparison
        consultation_date = datetime.strptime(consultation_date, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()

        # Check if any existing consultations overlap with the requested time
        overlapping_consultations = Consultation.query.filter(
            Consultation.psychologist_id == psychologist_id,
            Consultation.consultation_date == consultation_date,
            db.or_(
                db.and_(Consultation.start_time <= start_time, Consultation.end_time > start_time),
                db.and_(Consultation.start_time < end_time, Consultation.end_time >= end_time),
                db.and_(Consultation.start_time >= start_time, Consultation.end_time <= end_time)
            )
        ).all()

        # If any overlapping consultations exist, the psychologist is not available
        if overlapping_consultations:
            return False

        # Check if the psychologist's schedule allows for the requested time
        available_schedule = PsychologistSchedule.query.filter(
            PsychologistSchedule.psychologist_id == psychologist_id,
            PsychologistSchedule.is_available == True,
            PsychologistSchedule.start_time <= start_time,
            PsychologistSchedule.end_time >= end_time
        ).first()

        if not available_schedule:
            return False

        return True
