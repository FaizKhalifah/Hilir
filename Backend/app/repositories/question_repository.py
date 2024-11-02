from app.models.personalization_question import PersonalizationQuestion
from app.models.question_mental_health import QuestionMentalHealth
from app.models.child_personalization import ChildPersonalization
from app.models.mental_health_issue import MentalHealthIssue
from app.utils.db import db
from sqlalchemy import select

class QuestionRepository:
    @staticmethod
    def get_questions_for_mental_health_issues(child_id):
        """Retrieve questions based on the child’s mental health issues."""
        # Get mental health issues that exceed the threshold
        exceeded_issues = db.session.query(ChildPersonalization.mental_health_issue_id).filter(
            ChildPersonalization.child_id == child_id,
            ChildPersonalization.personalization_score >= select(MentalHealthIssue.threshold_score).where(
                MentalHealthIssue.id == ChildPersonalization.mental_health_issue_id
            ).scalar_subquery()
        ).subquery()

        # Get questions associated with those mental health issues
        questions = db.session.query(PersonalizationQuestion).join(
            QuestionMentalHealth, QuestionMentalHealth.question_id == PersonalizationQuestion.id
        ).filter(QuestionMentalHealth.mental_health_issue_id.in_(select(exceeded_issues.c.mental_health_issue_id))).all()

        return questions

    @staticmethod
    def get_score_impacts(question_id):
        """Retrieve the mental health impacts of answering a question."""
        return QuestionMentalHealth.query.filter_by(question_id=question_id).all()
