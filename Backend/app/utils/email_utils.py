from flask import current_app
from flask_mail import Message

def send_otp_email(email, otp_code):
    msg = Message("Your OTP Code", sender=current_app.config["MAIL_USERNAME"], recipients=[email])
    msg.body = f"Your OTP code is {otp_code}. It expires in 5 minutes."
    
    # Using `current_app` to access `mail`
    with current_app.app_context():
        mail = current_app.extensions['mail']
        mail.send(msg)
