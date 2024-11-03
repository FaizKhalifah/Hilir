from app.models.personalization_question import PersonalizationQuestion

class PersonalizationQuestionRepository:
    @staticmethod
    def get_questions_by_id_range(start_id, end_id):
        return PersonalizationQuestion.query.filter(
            PersonalizationQuestion.id >= start_id,
            PersonalizationQuestion.id <= end_id
        ).all()
