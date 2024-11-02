from app.repositories.parent_repository import ParentRepository
from app.utils.email_utils import send_otp_email
from app.models.parent import Parent
from app.utils.db import db
from app.repositories.personalization_question_repository import PersonalizationQuestionRepository

class ParentService:
    @staticmethod
    def register_parent(data):
        parent = Parent(
            username=data["username"],
            email=data["email"],
            is_verified=True  # Automatically set to verified
        )
        
        parent.set_password(data["password"])
        ParentRepository.save_parent(parent)
        
        return parent

    @staticmethod
    def confirm_otp(parent_id, otp_code):
        return ParentRepository.verify_otp(parent_id, otp_code)

    @staticmethod
    def resend_otp(email):
        parent = Parent.query.filter_by(email=email).first()

        if not parent:
            return None, "Parent not found"

        if parent.is_verified:
            return None, "Account already verified. No need to resend OTP."

        otp_code = ParentRepository.resend_otp(parent.id)
        send_otp_email(parent.email, otp_code)

        return parent, "OTP sent successfully"
    
    
    def get_personalized_questions():
        return PersonalizationQuestionRepository.get_questions_by_id_range(7, 15)

    @staticmethod
    def get_all_parents():
        return ParentRepository.get_all_parents()
