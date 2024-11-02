# app/services/psychologist_service.py

from app.repositories.psychologist_repository import PsychologistRepository

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
