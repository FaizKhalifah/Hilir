from app.repositories.parent_repository import ParentRepository
from app.utils.email_utils import send_otp_email
from app.models.parent import Parent
from app.utils.db import db
import app.models.assessment as Assessment

class ParentService:
    @staticmethod
    def register_parent(data):
        parent = Parent(
            username=data["username"],
            email=data["email"]
        )
        
        parent.set_password(data["password"])
        ParentRepository.save_parent(parent)
        
        otp_code = ParentRepository.generate_otp(parent.id)
        send_otp_email(parent.email, otp_code)
        
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
