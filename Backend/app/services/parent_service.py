from app.repositories.parent_repository import ParentRepository
from app.utils.email_utils import send_otp_email
from app.models.parent import Parent

class ParentService:

    @staticmethod
    def register_parent(data):
        parent = ParentRepository.create_parent(data)
        otp_code = ParentRepository.generate_otp(parent.id)
        send_otp_email(parent.email, otp_code)
        return parent

    @staticmethod
    def confirm_otp(parent_id, otp_code):
        return ParentRepository.verify_otp(parent_id, otp_code)

    @staticmethod
    def resend_otp(email):
        # Find the parent by email
        parent = Parent.query.filter_by(email=email).first()

        if not parent:
            return None, "Parent not found"

        if parent.is_verified:
            return None, "Account already verified. No need to resend OTP."

        # Generate a new OTP and send an email
        otp_code = ParentRepository.resend_otp(parent.id)
        send_otp_email(parent.email, otp_code)

        return parent, "OTP sent successfully"
