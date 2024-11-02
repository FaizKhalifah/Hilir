from datetime import datetime, timedelta
import random
from app.models.otp_verification import OTPVerification
from app.utils.db import db
from app.models.parent import Parent

class ParentRepository:

    @staticmethod
    def create_parent(data):
        parent = Parent(**data)
        db.session.add(parent)
        db.session.commit()
        return parent

    @staticmethod
    def generate_otp(parent_id):
        otp_code = str(random.randint(100000, 999999))
        expiration_date = datetime.utcnow() + timedelta(minutes=5)
        otp = OTPVerification(parent_id=parent_id, otp_code=otp_code, expiration_date=expiration_date)
        db.session.add(otp)
        db.session.commit()
        return otp_code

    @staticmethod
    def resend_otp(parent_id):
        # Check if an OTP already exists and update it
        existing_otp = OTPVerification.query.filter_by(parent_id=parent_id).first()

        if existing_otp:
            # Update the OTP code and expiration date
            existing_otp.otp_code = str(random.randint(100000, 999999))
            existing_otp.expiration_date = datetime.utcnow() + timedelta(minutes=5)
        else:
            # Create a new OTP record if none exists
            existing_otp = OTPVerification(
                parent_id=parent_id,
                otp_code=str(random.randint(100000, 999999)),
                expiration_date=datetime.utcnow() + timedelta(minutes=5)
            )
            db.session.add(existing_otp)

        db.session.commit()
        return existing_otp.otp_code
