# app/services/parent_service.py

from app.repositories.parent_repository import ParentRepository
from app.utils.email_utils import send_otp_email
from app.models.parent import Parent

class ParentService:

    @staticmethod
    def register_parent(data):
        # Create a new Parent instance
        parent = Parent(
            username=data["username"],
            email=data["email"]
        )
        
        # Hash the password before saving
        parent.set_password(data["password"])

        # Save the parent to the database
        ParentRepository.save_parent(parent)
        
        # Generate OTP and send it as part of the registration process
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

        # Generate a new OTP and send an email
        otp_code = ParentRepository.resend_otp(parent.id)
        send_otp_email(parent.email, otp_code)

        return parent, "OTP sent successfully"
