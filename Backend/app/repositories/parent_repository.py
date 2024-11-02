from datetime import datetime, timedelta
import random
from app.models.otp_verification import OTPVerification
from app.utils.db import db
from app.models.parent import Parent

class ParentRepository:
    @staticmethod
    def save_parent(parent):
        db.session.add(parent)
        db.session.commit()

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
        existing_otp = OTPVerification.query.filter_by(parent_id=parent_id).first()

        if existing_otp:
            existing_otp.otp_code = str(random.randint(100000, 999999))
            existing_otp.expiration_date = datetime.utcnow() + timedelta(minutes=5)
        else:
            existing_otp = OTPVerification(
                parent_id=parent_id,
                otp_code=str(random.randint(100000, 999999)),
                expiration_date=datetime.utcnow() + timedelta(minutes=5)
            )
            db.session.add(existing_otp)

        db.session.commit()
        return existing_otp.otp_code

    @staticmethod
    def verify_otp(parent_id, otp_code):
        otp_record = OTPVerification.query.filter_by(parent_id=parent_id, otp_code=otp_code).first()
        if otp_record and not otp_record.is_expired():
            return True
        return False
    
    @staticmethod
    def save_parent(parent):
        db.session.add(parent)
        db.session.commit()

    @staticmethod
    def get_all_parents():
        return Parent.query.all()
