# app/services/personalization_service.py

from app.repositories.personalization_response_repository import PersonalizationResponseRepository

class PersonalizationService:
    @staticmethod
    def save_response(child_id, question_id, response_score):
        return PersonalizationResponseRepository.save_response(child_id, question_id, response_score)

    @staticmethod
    def calculate_score(child_id):
        return PersonalizationResponseRepository.calculate_personalization_score(child_id)
