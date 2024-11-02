# app/repositories/personalization_response_repository.py

from app.models.personalization_response import PersonalizationResponse
from app.models.question_mental_health import QuestionMentalHealth
from app.models.child_personalization import ChildPersonalization
from app.models.mental_health_issue import MentalHealthIssue
from app.utils.db import db

class PersonalizationResponseRepository:
    @staticmethod
    def save_response(child_id, question_id, response_score):
        response = PersonalizationResponse(
            child_id=child_id,
            question_id=question_id,
            response_score=response_score
        )
        db.session.add(response)
        db.session.commit()
        return response

    @staticmethod
    def calculate_personalization_score(child_id):
        responses = PersonalizationResponse.query.filter_by(child_id=child_id).all()
        scores = {}

        for response in responses:
            question_links = QuestionMentalHealth.query.filter_by(question_id=response.question_id).all()
            for link in question_links:
                mental_health_issue_id = link.mental_health_issue_id
                score_impact = link.score_impact * response.response_score

                if mental_health_issue_id not in scores:
                    scores[mental_health_issue_id] = 0
                scores[mental_health_issue_id] += score_impact

        for mental_health_issue_id, total_score in scores.items():
            personalization = ChildPersonalization.query.filter_by(
                child_id=child_id, 
                mental_health_issue_id=mental_health_issue_id
            ).first()

            if personalization:
                personalization.personalization_score = total_score
            else:
                personalization = ChildPersonalization(
                    child_id=child_id,
                    mental_health_issue_id=mental_health_issue_id,
                    personalization_score=total_score
                )
                db.session.add(personalization)
        
        db.session.commit()

        # Check if any mental health issues exceed their threshold
        issues_above_threshold = []
        for mental_health_issue_id, score in scores.items():
            issue = MentalHealthIssue.query.get(mental_health_issue_id)
            if score >= issue.threshold_score:
                issues_above_threshold.append(issue.name)

        return issues_above_threshold
