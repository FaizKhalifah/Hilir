# app/services/personalization_service.py

from app.repositories.personalization_response_repository import PersonalizationResponseRepository
from app.repositories.question_repository import QuestionRepository
from app.models.child_personalization import ChildPersonalization
from app.utils.db import db
class PersonalizationService:
    @staticmethod
    def save_response(child_id, question_id, response_score):
        return PersonalizationResponseRepository.save_response(child_id, question_id, response_score)

    @staticmethod
    def calculate_score(child_id):
        return PersonalizationResponseRepository.calculate_personalization_score(child_id)
    @staticmethod
    def save_responses_and_update_scores(child_id, answers):
        # Save each response
        for answer in answers:
            PersonalizationResponseRepository.save_response(child_id, answer["question_id"], answer["response_score"])

            # Update personalization score based on the impact of the response
            impacts = QuestionRepository.get_score_impacts(answer["question_id"])
            for impact in impacts:
                ChildPersonalization.update_score(
                    child_id=child_id,
                    mental_health_issue_id=impact.mental_health_issue_id,
                    score_change=impact.score_impact * answer["response_score"]
                )

        # Commit all changes
        db.session.commit()