from datetime import datetime, timedelta
from app.models.base import BaseModel
from app.utils.db import db

class OTPVerification(BaseModel):
    __tablename__ = "otp_verifications"
    
    parent_id = db.Column(db.Integer, db.ForeignKey("parents.id"), nullable=False)
    otp_code = db.Column(db.String, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    
    parent = db.relationship("Parent", backref="otp_verifications", lazy=True)
    
    def is_expired(self):
        return datetime.utcnow() > self.expiration_date
